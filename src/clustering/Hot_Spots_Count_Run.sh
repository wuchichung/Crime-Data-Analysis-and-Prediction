cat ./NYPD_Complaint_Data_Historic_10000.csv | python3 ./Hot_Spots_Count_Mapper.py | sort -t ' ' -k 1 | python3 ./Hot_Spots_Count_Reducer.py > Hot_Spots_Count_Result.csv

# cat ../ml-20m/ratings.csv | python3 ./mapper.py | sort -t ' ' -k 1 | python3 ./reducer.py | sort -k 2 -n -r | head -100 | python3 ../post_processing.py ../ml-20m/movies.csv > result.csv
