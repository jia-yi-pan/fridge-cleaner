from datetime import datetime, timedelta
from entry_formatter import EntryFormatter
from fridge_data import FridgeData


fridge_data = FridgeData(access_mode="entry")


class EntryMode:

    def fridge_entry(self):
        entries = input("Please type all the items you would like to log in one line separated by a comma (ex. tomatoes, cheese): ").split(", ")
        for entry in entries:
            entry_formatter = EntryFormatter(entry)
            item_data_to_log = {
                entry: {
                    "Date Purchased": "",
                    "Approximate Expiration": ""
                }
            }
            date_today = datetime.now().strftime("%m/%d/%Y")
            date_next_week = (datetime.now() + timedelta(days=7)).strftime("%m/%d/%Y")
            manual_entry_prompt = input(
                f"Would you like to manually enter when you got '{entry}'? If manual entry is not selected, '{entry}' will be logged with the following details:\n"
                f"Date Purchased: {date_today}, Approximate Expiration: {date_next_week}\nType 'Y' for Yes or 'N' for No: ").upper().strip()
            if manual_entry_prompt == "Y":
                self.manual_entry_prompts(entry_formatter)
                item_data_to_log[entry]["Date Purchased"] = entry_formatter.date_purchased
                item_data_to_log[entry]["Approximate Expiration"] = entry_formatter.approx_expiration_date
                fridge_data.save_new_entry(item_data_to_log, entry_formatter.entry_type)
            elif manual_entry_prompt == "N":
                item_data_to_log[entry]["Date Purchased"] = date_today
                item_data_to_log[entry]["Approximate Expiration"] = date_next_week
                fridge_data.save_new_entry(item_data_to_log) #maybe make default i?
            else:
                print(f"That is not a valid entry! {entry} entry skipped.")

    def manual_entry_prompts(self, EntryFormatter):
        EntryFormatter.process_date_purchased()
        EntryFormatter.process_shelf_life()
        EntryFormatter.process_entry_type()
        EntryFormatter.process_approx_expiry()


