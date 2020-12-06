cat ./NYPD_Complaint_Data_Historic_10000.csv | python3 ./Hot_Spots_Count_Cat_Hour_Mapper.py | sort -t ' ' -k 1 | python3 ./Hot_Spots_Count_Cat_Hour_Reducer.py > Hot_Spots_Count_Cat_Hour_Result.csv
