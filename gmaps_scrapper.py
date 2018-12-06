import googlemaps
import csv
import os
from datetime import datetime
from utils import file_helpers
from utils import gcs_helpers as gcs

# config
gmaps_key = 'AIzaSyAggY6syUBWad_S_K5SaR3wGPV-h5zSXHo'
input_file = 'wilayah_administratif.csv'
output_dir = 'result'

# google maps client
gmaps = googlemaps.Client(key=gmaps_key)

# iterate list on CSV
with open(input_file) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			line_count += 1
		else:
			line_count += 1

			str_kelurahan = "{}, {}, {}, {}".format(row[1], row[3], row[5], row[7])
			str_kecamatan = "{}, {}, {}".format(row[3], row[5], row[7])
			str_kota = "{}, {}".format(row[5], row[7])
			str_provinsi = "{}".format(row[7])

			if not os.path.exists(output_dir):
				os.makedirs(output_dir)
			
			# geocode kelurahan
			if("KOTA" in str_kota):
				type_tingkat_4 = "kelurahan"
			else:
				type_tingkat_4 = "desa"
			geocode_kelurahan = str(gmaps.geocode(type_tingkat_4 + " " + str_kelurahan))
			f = open(output_dir + "/geocode_kelurahan_{}.json".format(str_kelurahan), "w")
			f.write(geocode_kelurahan)

			# geocode kecamatan
			geocode_kecamatan = str(gmaps.geocode("kecamatan " + str_kecamatan))
			f = open(output_dir + "/geocode_kecamatan_{}.json".format(str_kecamatan), "w")
			f.write(geocode_kecamatan)

			# geocode kota
			geocode_kota = str(gmaps.geocode(str_kota))
			f = open(output_dir + "/geocode_kota_{}.json".format(str_kota), "w")
			f.write(geocode_kota)

			# geocode provinsi
			geocode_provinsi = str(gmaps.geocode("provinsi " + str_provinsi))
			f = open(output_dir + "/geocode_provinsi_{}.json".format(str_provinsi), "w")
			f.write(geocode_provinsi)

			print "Processing {}".format(row)

	print "Processed {} lines.".format(line_count)