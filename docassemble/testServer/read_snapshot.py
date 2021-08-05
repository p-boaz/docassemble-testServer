from docassemble.base.util import variables_snapshot_connection, user_info

__all__ = ['analyze', 'datamap', 'datacats']

def analyze():
  conn = variables_snapshot_connection()
  cur = conn.cursor()
  cur.execute("select data->>'favorite_fruit' from jsonstorage where filename='" + user_info().filename + "'")
  counts = dict()
  for record in cur.fetchall():
    fruit = record[0].lower()
    if fruit not in counts:
      counts[fruit] = 0
    counts[fruit] += 1
  conn.close()
  return counts

def datamap():
  conn = variables_snapshot_connection()
  cur = conn.cursor()
  cur.execute("select data->>'data_category' from jsonstorage where filename='" + user_info().filename + "'")
  counts = dict()
  for record in cur.fetchall():
    data = record[0]
    if data not in counts:
      counts[data] = 0
    counts[data] += 1
  conn.close()
  return counts

def datacats():
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    cur.execute("select data from jsonstorage where filename='" + user_info().filename + "'")
    records = list()
    for record in cur.fetchall():
        records.append(record)
    conn.close()
    return records