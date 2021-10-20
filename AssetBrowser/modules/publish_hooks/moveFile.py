


class MoveFiles():
    def __init__(self):
        self.workspacePre = ""
        self.depotPre = ""


    def move(self, item_file, p4model):
        #todo waiting to change with setting
        if item_file.startWith("perforce"):
            #todo test download seed
            self.down_to_ws(item_file, p4model)

        elif item_file.startWith("export"):
            self.copy_to_ws(item_file)
            self.rm_tem_file(item_file)

        elif item_file.startWith("drag"):
            self.copy_to_ws(item_file)



    def down_to_ws(self, item_file, p4model):
        if item_file
