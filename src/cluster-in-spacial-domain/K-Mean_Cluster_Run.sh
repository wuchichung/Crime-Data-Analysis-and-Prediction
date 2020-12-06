cat ./NYPD_Complaint_Data_Historic_10000.csv | python3 ./K-Mean_Cluster_Mapper.py | sort -t ' ' -k 1 | python3 ./K-Mean_Cluster_Reducer.py > K-Mean_Cluster_Reducer_Result.csv
