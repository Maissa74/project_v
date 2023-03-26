curl https://fr.investing.com/commodities/gold > /home/ec2-user/project/code_source.html
data=$(cat /home/ec2-user/project/code_source.html | grep -oP '(?<="instrument-price-last">)[^<]+' | tr ',' '.' | sed 's/\.//')
time_data=$(date +"%Y-%m-%d %T")
echo $data
echo $time_data
echo "$data,$time_data" >> /home/ec2-user/project/data_and_time.csv
echo "$data,$time_data" >> /home/ec2-user/project/data_and_time.csv
