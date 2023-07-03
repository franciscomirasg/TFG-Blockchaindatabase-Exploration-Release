./city_hall.sh
echo "City Hall started"
sleep 3

./citizen_1.sh
echo "Citizen 1 started"
sleep 3

./citizen_2.sh
echo "Citizen 2 started"
sleep 3

./rec_company.sh
echo "Recycle Company started"
sleep 3

./container_1.sh
echo "Container 1 started"
sleep 3

./container_2.sh
echo "Container 2 started"
sleep 3

cd ..

rm -rf data/*

python -m scripts.load_governance
echo "Governance loaded"

echo "Deploy finished"