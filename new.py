# ! /usr/bin/env python3

import psycopg2
DB_NAME = "news"
artiview = ("create view article_view as select title,author,count(*) as"
            " numberofviews from articles,log where log.path like"
            " concat('%',articles.slug) group by articles.title,"
            "articles.author order by numberofviews desc")


elview = ("create view error_log_view as select date(time),round(100.0*sum("
          "case log.status when '200 OK' then 0 else 1 end)/count(log.status)"
          ",2) as PercentError from log group by date(time) "
          " order by PercentError desc")

# 1. What are the most popular three articles of all time?
X1 = "select title,numberofviews from article_view fetch first 3 rows only"

# 2. Who are the most popular article authors of all time?
X2 = """select authors.name,sum(article_view.numberofviews) as numberofviews
      from article_view,authors where authors.id = article_view.author
     group by authors.name order by numberofviews desc"""

# 3. On which days did more than 1% of requests lead to errors?
X3 = "select date,PercentError from error_log_view where PercentError > 1"

# to store results

Y1 = "\n1. The 3 most popular articles of all time are:\n"


Y2 = """\n2. The most popular article authors of
all time are:\n"""

Y3 = """\n3. Days with more than 1% of request that
lead to an error:\n"""


# returns query result
def queryresult(query):
    db = psycopg2.connect(database=DB_NAME)
    c = db.cursor()
    c.execute(elview)
    c.execute(artiview)
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


def Printquery_results(queryres):
    print (queryres[1])
    for result in queryres[0]:
        print ('\t' + str(result[0]) + ' ---> ' + str(result[1]) +
               'numberofviews')


def Printerror_query_results(queryres):
    print (queryres[1])
    for result in queryres[0]:
        print ('\t' + str([0]) + ' ---> ' + str(result[1]) + ' % errors')


# stores query result
x1_result = queryresult(X1), Y1
x2_result = queryresult(X2), Y2
x3_result = queryresult(X3), Y3

# print formatted output
Printquery_results(x1_result)
Printquery_results(x2_result)
Printerror_query_results(x3_result)
