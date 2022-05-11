def get_subclasses(cls):
    result = [cls]
    classes_to_inspect = [cls]
    while classes_to_inspect:
        class_to_inspect = classes_to_inspect.pop()
        for subclass in class_to_inspect.__subclasses__():
            if subclass not in result:
                result.append(subclass)
                classes_to_inspect.append(subclass)
    return result

def update_item_quantity_on_save(sender, instance, **kwargs):
    item_quantity = 0
    item_quantity =+ instance.quantity_issued
    instance.item.quantity -= item_quantity
    instance.item.save()

for subclass in get_subclasses(IssueRequisition):
    post_save.connect(update_item_quantity_on_save, subclass)