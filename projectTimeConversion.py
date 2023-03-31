
#Converts users time and return the total seconds 
def get_conversion(time: str, time_rate: str):
        time = int(time)
        if time_rate=="s":
                total_seconds = time
        elif time_rate == "m":
                total_seconds = time * 60
        elif time_rate == "h":
                total_seconds = time * 3600
        elif time_rate == "d":
                total_seconds = time * 86400
        else:
                total_seconds = time * 0
        return total_seconds