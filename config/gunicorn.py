bind = ':8080'
chdir = './core'
worker_class = 'aiohttp.GunicornWebWorker'
workers = 2
accesslog = '-'
errorlog = '-'