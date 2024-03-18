from wagtail.admin.panels import FieldPanel


class TargetFieldPanel(FieldPanel):
    """
    A FieldPanel that syncs the value of the field with other fields on the form.
    :param apply_if_live: (optional) If ``True``, the built in slug sync behaviour will apply irrespective of the published state.
        The default is ``False``, where the slug sync will only apply when the instance is not live (or does not have a live property).
    :param targets: (optional) This allows you to override the default target of the field named `slug` on the form.
        Accepts a list of field names, default is ``["slug"]``.
        Note that the slugify/urlify behaviour relies on usage of the ``wagtail.admin.widgets.slug`` widget on the slug field.
    """

    def __init__(
        self,
        *args,
        apply_if_live=False,
        targets=["slug"],
        **kwargs,
    ):
        self.targets = targets
        self.apply_if_live = apply_if_live
        super().__init__(*args, **kwargs)

    def clone_kwargs(self):
        return {
            **super().clone_kwargs(),
            "apply_if_live": self.apply_if_live,
            "targets": self.targets,
        }

    class BoundPanel(FieldPanel.BoundPanel):
        apply_actions = [
            "focus->w-sync#check",
            "blur->w-sync#apply",
            "change->w-sync#apply",
            "keyup->w-sync#apply",
        ]

        def get_context_data(self, parent_context=None):
            field = self.bound_field.field
            if field and not self.read_only:
                field.widget.attrs.update(**self.get_attrs())
            return super().get_context_data(parent_context)

        def get_attrs(self):
            """
            Generates a dict of widget attributes to be updated on the widget
            before rendering.
            """

            panel = self.panel
            widget = self.bound_field.field.widget

            attrs = {}

            if self.get_should_apply():
                controllers = [widget.attrs.get("data-controller", None), "w-sync"]
                attrs["data-controller"] = " ".join(filter(None, controllers))

            actions = [widget.attrs.get("data-action", None)] + self.apply_actions
            attrs["data-action"] = " ".join(filter(None, actions))

            targets = [
                self.get_target_selector(target)
                for target in panel.targets
                if target in self.form.fields
            ]
            attrs["data-w-sync-target-value"] = ", ".join(filter(None, targets))

            return attrs

        def get_should_apply(self):
            """
            Check that the title field should apply the sync with the target fields.
            """
            if self.panel.apply_if_live:
                return True

            instance = self.instance
            if not instance:
                return True

            is_live = instance.pk and getattr(instance, "live", False)
            return not is_live

        def get_target_selector(self, target):
            """
            Prepare a selector for an individual target field.
            """
            field = self.form[target]
            return f"#{field.id_for_label}"
