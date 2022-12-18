sudo apt install python-dev
sudo apt install python3-pip

python3 -m venv ../venv
source ../venv/bin/activate

pip3 install numpy
pip3 install toml
pip3 install pandas
pip3 install matplotlib
pip3 install prettytable
pip3 install scikit-optimize
pip3 install pyinform


# web Requriemnts
pip3 install WebApp/requirements.txt
pip install django-jsonfield

python3  manage.py runserver
