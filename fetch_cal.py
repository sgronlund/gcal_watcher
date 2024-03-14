from ics import Calendar
import aiohttp
import asyncio
import pandas as pd
import arrow
import re

async def fetch_ics_files():
	async with aiohttp.ClientSession() as session:
		df = pd.read_csv("ics.csv", quotechar="'")
		for idx, item in df.iterrows():
			ics_url = item["source"]
			cal_type = item["cal"]
			async with session.get(ics_url) as response:
				events_in_scope = []
				utcnow = arrow.utcnow()
				now = utcnow.shift(hours=1)	
				last_six = utcnow.shift(months=-12)
				yesterday = utcnow.shift(days=-1)
				content = await response.text()
				c = Calendar(content)
				for e in c.events:
					txt = str(e.serialize())
					m = re.search("RRULE", txt)
					arw_str = None
					if m:
						n = re.search("UNTIL=", txt)
						if n:
							n_stop = 0	
							for i in range(n.end(), len(txt)):
								if txt[i] == ';':
									n_stop = i
									break
								if txt[i] == '\n':
									n_stop = i - 1
									break
							date_str = txt[n.end():n_stop]
							arw_str = arrow.get(date_str)
					if arw_str:
						if arw_str > utcnow: # recurring event that hasn't ended yet
							events_in_scope.append(e)	
					else: # => non-recurring event, just check in range of pref range
						if e.begin > utcnow:
							events_in_scope.append(e)	
				if len(events_in_scope) > 0:
					with open(f"{cal_type}_{now.format(fmt='YYYYMMDD_HHmm')}", "w") as file:
						for e in events_in_scope:
							file.write(str(e))

if __name__ == "__main__":
	asyncio.run(fetch_ics_files())
