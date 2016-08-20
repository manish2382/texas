__author__ = 'manish'
from django.core.management import BaseCommand
from texasparser.models import Files
from django.db import transaction
import csv


EXPECTED_ARGUMENT = 'file_path'

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(EXPECTED_ARGUMENT, nargs='+', type=str, help='Path for the file to be processed')

    def handle(self, *args, **options):

        # check if duplicate rows exists converge them to same row
        def fix_data(cache, fix_row):
            cache_key = str(fix_row[0:len(fix_row)-1])
            try:
                cache[cache_key].append(fix_row[-1])
            except KeyError:
                cache[cache_key] = [fix_row[-1]]

            return cache[cache_key]

        file_path = options[EXPECTED_ARGUMENT]
        caching = {}
        result = []
        try:
            with open(file_path[0], 'rb') as csvfile:

                # understand the format of input file and create reader
                dialect = csv.Sniffer().sniff(csvfile.read(1024))
                csvfile.seek(0)
                reader = csv.reader(csvfile, dialect)

                # check if header is associated with csv file
                if csv.Sniffer().has_header(csvfile.read(1024)):
                    csvfile.seek(0)
                    headers = reader.next()
                else:
                    # if header is not present than create numeric headers
                    headers = []
                    header_count = len(reader.next())
                    for i in range(header_count):
                        headers.append(str(i))
                    # reset reader
                    csvfile.seek(0)

                # process each row of input file
                for row in reader:
                    # map each column vale with corresponding header
                    elements = {}
                    for header, element in zip(headers, row):
                        elements[header] = element

                    # if there is any duplicate row, aggregate all images
                    elements[headers[-1]] = fix_data(caching, row)

                    # collect the data together
                    if not result or result[-1] != elements:
                        result.append(elements)

            # save the processed data to database.
            # In case of any failure
            with transaction.atomic():
                for obj in result:
                    Files.objects.create(data=obj)

        except IOError:
            print "No file found on given path"
