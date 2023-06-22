import subprocess
import time

# Names of your spiders
spiders = ["price_finder_bst"]
runs_per_spider = 5

# Placeholder for results
results = {}

for spider in spiders:
    times = []
    for _ in range(runs_per_spider):
        start_time = time.time()
        subprocess.call(f'scrapy crawl {spider}', shell=True)
        end_time = time.time()
        times.append(end_time - start_time)
    avg_time = sum(times) / runs_per_spider
    results[spider] = avg_time

# Print the results
for spider, avg_time in results.items():
    print(f'Average time for {spider}: {avg_time} seconds')
