from datetime import datetime, timedelta

class EntryFormatter:
    def __init__(self, entry_item):
        self.entry_item = entry_item
        self.date_purchased = ""
        self.month_purchased = ""
        self.day_purchased = ""
        self.year_purchased = ""
        self.shelf_life_unit = ""
        self.shelf_life_status = ""
        self.entry_type = ""
        self.approx_expiration_date = ""

    def process_entry_type(self):
        run = True
        while run:
            entry_type = input(
                f"What best describes '{self.entry_item}'? Type 'M' for meal or 'I' for ingredient: ").strip().upper()
            if entry_type == "M":
                self.entry_type = "meal"
                break
            elif entry_type == "I":
                self.entry_type = "ingredient"
                break
            else:
                print("That is not a valid letter. Please try again.")

    def process_shelf_life(self):
        run = True
        while run:
            shelf_life_unit = input(
                f"Type the letter that corresponds with the increment best describing how long until '{self.entry_item}' goes bad from your entered purchased date.\n"
                f"'M' for months, 'W' for weeks, or 'D' for days: ").strip().upper()
            if shelf_life_unit == "M":
                self.shelf_life_unit = "months"
                break
            elif shelf_life_unit == "W":
                self.shelf_life_unit = "weeks"
                break
            elif shelf_life_unit == "D":
                self.shelf_life_unit = "days"
                break
            else:
                print("That is not a valid letter Please try again.")

        shelf_life_status = input(
            f"How many {self.shelf_life_unit} until '{self.entry_item}' goes bad? Please type a number: ")
        self.shelf_life_status = shelf_life_status + " " + self.shelf_life_unit

    def process_date_purchased(self):
        self.year_purchased = str(datetime.now().year)
        run = True
        while run:
            date_purchased = input(f"When did you purchase '{self.entry_item}'? Please use the format MM/DD: ").strip()
            date_purchased_values = date_purchased.split("/")
            if len(date_purchased_values) == 2 and len(date_purchased) == 5:
                self.date_purchased = date_purchased + "/" + self.year_purchased
                self.month_purchased = int(date_purchased_values[0])
                self.day_purchased = int(date_purchased_values[1])
                self.year_purchased = int(self.year_purchased)
                break
            else:
                print("Incorrect Entry")

    def process_approx_expiry(self):
        purchase_datetime_obj = datetime.strptime(self.date_purchased, "%m/%d/%Y")
        amount_to_expiry = int(self.shelf_life_status.split(" ")[0])
        # what to do when amount exceeds unit like 24 months
        if self.shelf_life_unit == "months":
            expiry_month = self.month_purchased + amount_to_expiry
            expiry_year = self.year_purchased
            if expiry_month < 10 or expiry_month > 12:
                if expiry_month > 12:
                    expiry_month = expiry_month % 12
                    expiry_year = self.year_purchased + 1
                expiry_month = "0" + str(expiry_month)
            self.approx_expiration_date = f"{expiry_month}/{self.day_purchased}/{expiry_year}"
        elif self.shelf_life_unit == "weeks":
            days_to_expiry = amount_to_expiry * 7
            expiry_date_obj = purchase_datetime_obj + timedelta(days=days_to_expiry)
            self.approx_expiration_date = datetime.strftime(expiry_date_obj, "%m/%d/%Y")
        else:
            expiry_date_obj = purchase_datetime_obj + timedelta(days=amount_to_expiry)
            self.approx_expiration_date = datetime.strftime(expiry_date_obj, "%m/%d/%Y")


