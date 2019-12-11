import csv
import datetime

result = []

sentiment_date=[]
sentiment_Score=[]
sentiment_company=[]
with open("GP-Square-Pharma-2010-2019.csv", "r", encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
            Date=(row["Date"])
            sentiment_Score.append(row["Binary Score"])
            sentiment_company.append(row["Company"])
            #print(len(word))
            sentiment_date.append(Date[:8])

dt = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2019, 10, 1)
step = datetime.timedelta(days=1)
while dt < end:
    li=(dt.strftime('%d-%m-%Y'))
    li1=li[0:6]
    li2=li[8:10]
    li3=li1+li2
    result.append(li3)
    dt += step
i=0
index=[]
for date in result:
    for sent_date in sentiment_date:
        if date==sent_date:
            index.append(i)
    i+=1
k=0
Score = [5 for x in range(3560)]
for i in range(len(result)):
    for j in index:
        if i==j:
            Score[j]=sentiment_Score[k]
            k+=1

m=0
gp_index=[] 
sq_index=[]
both=[]   
for c in sentiment_company:
    if c=='gpdata':
        gp_index.append(m)
    elif c=='sqdata':
       sq_index.append(m)
    else:
        both.append(m)
    m+=1
gp = [5 for x in range(len(result))]
sq= [5 for x in range(len(result))]
Both=[5 for x in range(len(result))]
l=0
n=0
gp_ind=[] 
sq_ind=[]
both_ind=[]
i=0
p=0
for date in result:

    for sent_date in sentiment_date:
        if date==sent_date:
            for j in gp_index:
                if j==i:
                    gp[l]=(sentiment_Score[i])
                    gp_ind.append(l)
        
            for k in sq_index:
                if k==i:
                    sq[n]=(sentiment_Score[i])
                    sq_ind.append(n)
            for m in both:
                if m==i:
                    Both[p]=(sentiment_Score[i])
                    both_ind.append(p)
            i+=1
    l+=1
    n+=1
    p+=1

gp_stored=1
sq_stored=1
both_stored=1
for i in range(len(result)):
    for j in gp_ind:
        if i==j:
            gp_stored=gp[i]
    gp[i]=gp_stored
    
    for l in sq_ind:
        if i==l:
            sq_stored=sq[i]
    sq[i]=sq_stored
    
    for q in both_ind:
        if i==q:
            both_stored=Both[i]
    Both[i]=both_stored



       
gp_csv = [0 for x in range(3560)]
sq_csv= [0 for x in range(3560)]
stored=1
both_com = [0 for x in range(3560)]
    

stored =[]
for i in range(len(result)):
    for j in index:
            
        if i==j:
            
            stored=Score[i]
    
    Score[i]=stored
    
with open('gp_sentiment.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Date","Score"])
    for i in range(len(gp)):
    	writer.writerow([result[i],gp[i]])
        
with open('sq_sentiment.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Date","Score"])
    for i in range(len(sq)):
    	writer.writerow([result[i],sq[i]])
with open('both_sentiment.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["Date","Score"])
    for i in range(len(both)):
    	writer.writerow([result[i],both[i]])

    


    