# Tools Sederhana Generate Qris, Power By Hotel Murah
# Github : github.com/RozhBasXYZ

import requests, re, json, urllib, time, os
ses = requests.Session()

class qris_kode:
	def __init__(self):
		self.daftar_harga = {"1k": "233", "2k": "234", "3k": "235", "4k": "236", "5k": "237", "10k": "36", "20k": "37", "25k": "38", "50k": "39", "75k": "40", "100k": "41"}
		self.csrf = ses.get("https://www.hotelmurah.com/pulsa/top-up-dana").cookies["hotelmurah_csrf_cookie_name"]
	
	def coki(self, ses):
		return {"cookie": ";".join([key+"="+value.replace('"','') for key, value in ses.cookies.get_dict().items()])}
	
	def nom_harga(self, nominal):
		return "{:,.0f}".format(nominal).replace(",", ".")
	
	def menu_utama(self):
		menu = input(f"""  - GENERATOR QRIS TO DANA BY ROZHBAS -
[1] 1.000     [6] 10.000     [11] 100.000
[2] 2.000     [7] 20.000     [12] 120.000
[3] 3.000     [8] 25.000     [13] 150.000
[4] 4.000     [9] 50.000     [14] 175.000
[5] 5.000     [0] 75.000     [15] 200.000
{'-'*23}
[?] pilih : """)
		if menu in ["1", "01"]: self.beli = self.daftar_harga["1k"]
		elif menu in ["2", "02"]: self.beli = self.daftar_harga["2k"]
		elif menu in ["3", "03"]: self.beli = self.daftar_harga["3k"]
		elif menu in ["4", "04"]: self.beli = self.daftar_harga["4k"]
		elif menu in ["5", "05"]: self.beli = self.daftar_harga["5k"]
		elif menu in ["6", "06"]: self.beli = self.daftar_harga["10k"]
		elif menu in ["7", "07"]: self.beli = self.daftar_harga["20k"]
		elif menu in ["8", "08"]: self.beli = self.daftar_harga["25k"]
		elif menu in ["9", "09"]: self.beli = self.daftar_harga["50k"]
		elif menu in ["10", "0"]: self.beli = self.daftar_harga["75k"]
		elif menu in ["11", "qq"]: self.beli = self.daftar_harga["100k"]
		else: exit("[!] mohon maaf limit tersebut belum tersedia")
		self.nomor = input("[?] nomor : 62")
		self.submit_harga()
	
	def submit_harga(self):
		try:
			date = {
			     "cust_number": "0"+self.nomor,
			     "hm_csrf_hash_name": self.csrf,
			     "id": self.beli,
			     "tipe_produk": "11",
			     "web": "web"
			}
			self.data_key = ses.post("https://www.hotelmurah.com/pulsa/index.php/ewallet/isOrderValidated", data=date, cookies=self.coki(ses)).json()["data"]
			self.submit_order()
		except Exception as e: exit("[!] opps error submit harga", e)
	
	def submit_order(self):
		try:
			date = {
			     "data": self.data_key,
			     "hm_csrf_hash_name": self.csrf,
			     "id_pay": "101",
			     "no_ovo": "0"+self.nomor,
			     "payment_pay": "gopay",
			     "payment_type": "100",
			     "source": "",
			     "stats": "",
			     "type_pembayaran": "m13",
			     "validasiTelkomsel": ""
			}
			self.token = ses.post("https://www.hotelmurah.com/pulsa/ewallet/submitorder", data=date, cookies=self.coki(ses)).json()["tokenPayment"]
			self.get_qris_kode()
		except Exception as e: exit("[!] opps error submit order", e)
	
	def get_qris_kode(self):
		try:
			link = ses.get("https://app.midtrans.com/snap/v1/pay?origin_host=https://www.hotelmurah.com&digest=5117adc7a2e42c4f5897d401e36a4c3c0c2353b68e6687d0978fc0f1c53a504e&client_key=VT-client-qtmtyIB7aYfbcneb#/", cookies=self.coki(ses)).text
			head = {
			     "X-NewRelic-ID": re.findall('xpid:"(.*?)"', link)[0],
			     "X-Source": "snap",
			     "X-Source-App-Type": "popup",
			     "X-Source-Version": "",
			     "newrelic": self.data_key,
			     "Accept": "application/json",
			     "Content-Type": "application/json",
			     "Secret-Key": "RozhBasGantengCoy"
			}
			date = json.dumps({
			     "payment_params": {"acquirer": ["gopay"]
			     }, "payment_type":"qris"
			})
			qris = ses.post(f"https://app.midtrans.com/snap/v2/transactions/{self.token}/charge", data=date, headers=head).json()["qris_url"]
			nominal = int(ses.get("https://app.midtrans.com/snap/v1/transactions/"+self.token, cookies=self.coki(ses)).json()["transaction_details"]["gross_amount"])
			print(f"[!] harga : {self.nom_harga(nominal)}")
			print(f"[!] links : {qris}")
			open(f"/sdcard/rozhQR-{str(time.time()).split('.')[0]}.jpg", "wb").write(urllib.request.urlopen(qris).read())
			print("[!] qris sukses disimpan ke galeri")
		except Exception as e: exit("[!] opps error get qris", e)
			
if __name__ == "__main__":
	os.system("clear"); qris_kode().menu_utama()