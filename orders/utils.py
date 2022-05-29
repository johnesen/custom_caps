from django.utils.translation import gettext_lazy as _


class OrderStatus:
    SUCCESS = 'success'
    ONTHEWAY = 'ontheway'
    PEPARING = 'preparing'

    @classmethod
    def choices(cls):
        return (
            (cls.SUCCESS, _(cls.SUCCESS)),
            (cls.ONTHEWAY, _(cls.ONTHEWAY)),
            (cls.PEPARING, _(cls.PEPARING)),
        )

# class OrderState:
#     ACTIVE = 'active'
#     INACTIVE = 'inactive'
#     DELETED = 'deleted'
#     ON_REVIEW = 'on_review'

#     @classmethod
#     def choices(cls):
#         return (
#             (cls.ACTIVE, _(cls.ACTIVE)),
#             (cls.INACTIVE, _(cls.INACTIVE)),
#             (cls.DELETED, _(cls.DELETED)),
#             (cls.ON_REVIEW, _('on review'))
#         )