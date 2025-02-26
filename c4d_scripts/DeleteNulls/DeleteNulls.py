import c4d

def delete_empty_nulls(obj, doc):
    if obj is None:
        return

    # 先递归处理子对象
    child = obj.GetDown()
    while child:
        next_child = child.GetNext()
        delete_empty_nulls(child, doc)
        child = next_child

    # 检查当前对象是否为Null类型
    if obj.GetType() == c4d.Onull:
        # 检查是否有子对象
        if obj.GetDown() is None:
            # 没有子对象，直接删除
            doc.AddUndo(c4d.UNDOTYPE_DELETE, obj)
            obj.Remove()
        else:
            # 有子对象，删除但不包括子对象
            parent = obj.GetUp()
            child = obj.GetDown()
            # 保存子对象的全局矩阵
            child_matrices = {}
            while child:
                child_matrices[child] = child.GetMg()
                child = child.GetNext()

            child = obj.GetDown()
            # 将子对象移动到父对象下
            while child:
                next_child = child.GetNext()
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, child)
                child.InsertAfter(obj)
                # 恢复子对象的全局矩阵
                child.SetMg(child_matrices[child])
                child = next_child

            doc.AddUndo(c4d.UNDOTYPE_DELETE, obj)
            obj.Remove()


def main():
    doc = c4d.documents.GetActiveDocument()
    doc.StartUndo()

    # 获取所选对象
    selected_objects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    for obj in selected_objects:
        delete_empty_nulls(obj, doc)

    doc.EndUndo()

    # 更新Cinema 4D界面
    c4d.EventAdd()


if __name__ == "__main__":
    main()