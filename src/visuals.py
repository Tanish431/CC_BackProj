import matplotlib.pyplot as plt

plt.show(block=True)

def plot_endpoint_pie(req_info):
    labels = []
    sizes = []
    others = 0.0

    for endpoint, data in req_info["endpoint_counts"].items():
        #For clarity
        if data["percent"] >= 3.0:
            labels.append(endpoint)
            sizes.append(data["percent"])
        else:
            others += data["percent"]
    
    #Collapsing data
    if others > 0:
        labels.append("Others")
        sizes.append(others)

    try:
        plt.figure(figsize=(5,5))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
        plt.title("Endpoint Popularity (%)")
        plt.show()
    except Exception as e:
        print(f"Error plotting pie chart: {e}")

def plot_strategy_pie(app):
    labels = list(app["strategy_counts"].keys())
    sizes = list(app["strategy_counts"].values())

    if not sizes or not labels:
        print("No strategy data available for plotting.")
        return
    
    try:
        plt.figure(figsize=(5,5))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
        plt.title("Strategy Usage (%)")
        plt.show()
    except Exception as e:
        print(f"Error plotting pie chart: {e}")
