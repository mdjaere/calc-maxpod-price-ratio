prices = [line.replace("\n", "").strip().split() for line in open("./prices.txt") if "#" not in line]

# vCPU	ECU	Memory (GiB)	Instance Storage (GB)	Linux/UNIX Usage
# Example price ['t3.2xlarge', '8', 'Variable', '32', 'GiB', 'EBS', 'Only', '$0.3776', 'per', 'Hour']
# --->  t3.2xlarge	8	Variable	32 GiB	EBS Only	$0.3776 per Hour
# Example price ['m5ad.8xlarge','32', 'N/A', '128', 'GiB', '2', 'x', '600', 'NVMe', 'SSD', '$1.92', 'per', 'Hour']
# --->  m5ad.8xlarge	32	N/A	128 GiB	2 x 600 NVMe SSD	$1.92 per Hour

price_dict = {}
for price_item in prices:
  name = price_item[0]
  cpu = price_item[1]
  mem = price_item[3]
  price = float(price_item[-3].strip("$"))
  price_dict[name] = {"price": price, "name": name, "mem": mem, "cpu": cpu}

max_pod = [line.replace("\n", "").strip().split() for line in open("./max-pod.txt") if "#" not in line]

for pod_name, pod_max in max_pod:
  pod_max = int(pod_max)
  if pod_name in price_dict:
    price = price_dict[pod_name]["price"]
    pod_price = price/pod_max
    price_dict[pod_name]["pod_max"] = pod_max
    price_dict[pod_name]["pod_price"] = round(pod_price, 4)
    price_dict[pod_name]["price_per_day"] = round(price_dict[pod_name]["price"] * 24, 2)

sorted_prices = sorted( price_dict.values(), key=lambda i: i["pod_price"] ) 

for e in sorted_prices:
  print(f"NAME: {e['name']:<15} CORES: {e['cpu']:<15} MEMORY (GB): {e['mem']:<15}  HOUR PRICE ($): {e['price']:<15} DAY PRICE ($): {e['price_per_day']:<15} MAX PODS: {e['pod_max']:<15} POD PRICE: {e['pod_price']:<15}") 
