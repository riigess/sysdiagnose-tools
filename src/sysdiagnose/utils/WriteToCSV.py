import csv
import os

class WriteToCSV:
	def write_rows_to_csv(self, rows:list[list[str]]=[], output_dir:str=os.environ['HOME']):
		with open(f"{output_dir}/Desktop/powerlogs.csv", "w", newline="") as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for row in rows:
				spamwriter.writerow(row)
