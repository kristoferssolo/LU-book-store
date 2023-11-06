import npyscreen as nps


class BookGrid(nps.GridColTitles):
    def custom_print_cell(self, actual_cell, cell_display_value):
        if actual_cell == 4:
            if int(cell_display_value) == 0:
                actual_cell.color = "DANGER"
            elif int(cell_display_value) < 5:
                actual_cell.color = "WARNING"
            else:
                actual_cell.color = "DEFAULT"
        return super().custom_print_cell(actual_cell, cell_display_value)
