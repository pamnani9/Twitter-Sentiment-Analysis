from tkinter import *
import random
from tkinter import messagebox
from tkinter import ttk
import tweepy
import pandas as pd
import numpy as np
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns
import textblob
import re
from PIL import ImageTk,Image


# Access
acces_token='966289632815144960-7BYnTY1ABbykfiNJNkZtjfhfmJfSsUl'
acces_token_secret='irZDHPTcMNYSikwCI9UohSlayGbGcLVEccvGptwaWOyil'

#Consumer
consumer_key='enMyXDNHgcbBiRMUv9TfPHRW9'
consumer_secret='Yp4e9s856kllbT5JyZYxL1Pk4i88R9Mk9FaJT7rH0nBHlGO3Ks'


def fun1(scr,dt):
    a=scr
    try:
        data=pd.read_csv(""+dt+".csv")
    except:
        messagebox.showinfo("Error","File Location not found..!")
        scr.destroy()   
        main()
    fun3(data,a)

def fun2(scr,dt):
    a=scr
    try:
        def twitter_setup():
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(acces_token, acces_token_secret)
            api = tweepy.API(auth)
            return api

        extractor = twitter_setup()
        #tweets=[tweet for tweet in tweepy.Cursor(extractor.user_timeline,screen_name=str(dt)).items()]
        tweets = extractor.user_timeline(screen_name=str(dt), count = 200)
    except:
        messagebox.showinfo("Error","Timeline did not matched..Please try again.")
        scr.destroy()
        main()

    
    
    #print("number of tweets extracted: {}.\n".format(len(tweets)))
    messagebox.showinfo('Length of tweets',"number of tweets extracted: {}.\n".format(len(tweets)))
    

    data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
 
    
    # We add relevant data
    data['len'] = np.array([len(tweet.text) for tweet in tweets])
    data['ID'] = np.array([tweet.id for tweet in tweets])
    data['Date'] = np.array([tweet.created_at for tweet in tweets])
    data['Source'] = np.array([tweet.source for tweet in tweets])
    data['Likes'] = np.array([tweet.favorite_count for tweet in tweets])
    data['RTs'] = np.array([tweet.retweet_count for tweet in tweets])

    fun3(data,a)
    

def fun3(data,a):
    # We extract the mean of length
    mean = np.mean(data['len'])
    #print("the length's average in tweets: {}".format(mean))
    messagebox.showinfo("Average Length","The length's average in tweets: {}".format(mean))

    # We extract the tweet with more FAVs and mote RTs:
 
    fav_max = np.max(data['Likes'])
    rt_max = np.max(data['RTs'])
 
    fav = data[data.Likes == fav_max].index[0]
    rt = data[data.RTs == rt_max].index[0]
 
    # Max FAVs:
    #print("the tweet with more likes is: \n{}".format(data['tweets'][fav]))
    #print("Number of likes: {}".format(fav_max))
    #print("{} character.\n".format(data['len'][fav]))
    messagebox.showinfo("Fav","The tweet with more like is : {}\n".format(data['tweets'][fav]+"Number of likes : {}\n".format(fav_max)+
                                                                    "{} character.\n".format(data['len'][fav])))
 
    # Max RTs:
    #print("The tweet with more retweets is: \n{}".format(data['tweets'][rt]))
    #print("Number of retweets: {}".format(rt_max))
    #print("{} character.\n".format(data['len'][rt]))
    messagebox.showinfo("Retweets","The tweet with more retweet is : {}\n".format(data['tweets'][rt]+"Number of retweets : {}\n".format(rt_max)+
                                                                    "{} character.\n".format(data['len'][rt])))
 

    tlen = pd.Series(data = data['len'].values)   #, index=data['Data'])
    tfav = pd.Series(data = data['Likes'].values)   #, index=data['Data'])
    tret = pd.Series(data = data['RTs'].values) #, index=data['Data']

    # Lenghts along time:
    tlen.plot(figsize=(16,4), color='r');

    # Likes vs retweets visualization:
    tfav.plot(figsize=(16,4), label="Likes", legend=True)

    tret.plot(figsize=(16,4), label="Retweets", legend=True);

    
    # We obtain all possible sources:
    sources = []
    for source in data['Source']:
        if source not in sources:
            sources.append(source)

    # We print sources list:
    print("Creation of content sources:")
    for source in sources:
        print("* {}".format(source))

    # We create a numpy vector mapped to labels:
    percent = np.zeros(len(sources))
 
    for source in data['Source']:
        for index in range(len(sources)):
            if source == sources[index]:
                percent[index] += 1
                pass
 
    percent /= 100
 
    # Pie chart:
    #pie_chart = pd.Series(percent, index=sources,name='')
    #pie_chart.plot.pie(fontsize=11, autopct='%.2f', figsize=(6, 6));
   
    
    def clean_tweet(tweet):
        '''Utility function to clean the text in a tweet by removing 
    links and special characters using regex.'''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analize_sentiment(tweet):
        '''Utility function to classify the polarity of a tweet
    using textblob.'''
        analysis = textblob.TextBlob(clean_tweet(tweet))
        #return str(analysis.sentiment.polarity)
        if analysis.sentiment.polarity == 0:
            return 0
        elif analysis.sentiment.polarity > 0:
            return 1
        else:
            return -1
    
    l=[]
    for tweet in data['tweets']:
        l.append(analize_sentiment(tweet))

    data['SA']=np.array(l)

    # We construct lists with classified tweets:
 
    pos_tweets = [ tweet for index, tweet in enumerate(data['tweets']) if data['SA'][index] > 0]
    neu_tweets = [ tweet for index, tweet in enumerate(data['tweets']) if data['SA'][index] == 0]
    neg_tweets = [ tweet for index, tweet in enumerate(data['tweets']) if data['SA'][index] < 0]
        
    # We print percentages:
 
    #print("Percentage of positive tweets: {}%".format(len(pos_tweets)*100/len(data['tweets'])))
    #print("Percentage of neutral tweets: {}%".format(len(neu_tweets)*100/len(data['tweets'])))
    #print("Percentage of negative tweets: {}%".format(len(neg_tweets)*100/len(data['tweets'])))
    messagebox.showinfo("Result","Percentage of positive tweets: {}%\n".format(len(pos_tweets)*100/len(data['tweets']))+
    "Percentage of neutral tweets: {}%\n".format(len(neu_tweets)*100/len(data['tweets']))+
    "Percentage of negative tweets: {}%\n".format(len(neg_tweets)*100/len(data['tweets'])))

    p=(len(pos_tweets)*100/len(data['tweets']))
    ne=(len(neu_tweets)*100/len(data['tweets']))
    n=(len(neg_tweets)*100/len(data['tweets']))

    result(a,p,ne,n)
    
    
    

def page_two(scr1):
    scr1.destroy()
    scr=Tk()
    var=StringVar(scr)
    var.set("NarendraModi")
    scr.geometry("700x350")
    scr.title("Twitter Data Sentiment Analysis")
    scr.resizable(False, False)
    mainf2=Frame(scr,height=618,width=1366)
    c=Canvas(mainf2,height=618,width=1366)
    c.pack()
    ent=Entry(mainf2,width=25,bd=2,textvariable=var,font=('Times New Roman',18,'bold'))
    ent.place(x=200,y=60)
    b=Button(mainf2,command=lambda :fun1(scr,var.get()),height=2,width=10,text='Go',font=('Times New Roman',12,'bold'),bg='green',fg='white')
    b.place(x=300,y=100)
    backs=PhotoImage(file="abc.gif")
    c.create_image(350,172,image=backs)
    lab=Label(mainf2,text= "Created by Prabhat Ranjan Dubey",fg="red",font=('Times New Roman',20,'bold'),bg='sky blue')
    lab.place(x=170,y=315)
    mainf2.pack(fill=BOTH,expand=1)
    dt=var.get()
    scr.mainloop()

def page_three(scr1):
    scr1.destroy()
    scr=Tk()
    var=StringVar(scr)
    var.set("NarendraModi")
    scr.geometry("700x350")
    scr.title("Twitter Data Sentiment Analysis")
    scr.resizable(False, False)
    mainf2=Frame(scr,height=618,width=1366)
    c=Canvas(mainf2,height=618,width=1366)
    c.pack()
    ent=Entry(mainf2,width=25,bd=2,textvariable=var,font=('Times New Roman',18,'bold'))
    ent.place(x=200,y=60)
    b=Button(mainf2,command=lambda :fun2(scr,str(var.get())),height=2,width=10,text='Go',font=('Times New Roman',12,'bold'),bg='green',fg='white')
    b.place(x=300,y=100)
    backs=PhotoImage(file="abc.gif")
    c.create_image(350,172,image=backs)
    lab=Label(mainf2,text= "Created by Prabhat Ranjan Dubey",fg="red",font=('Times New Roman',20,'bold'),bg='sky blue')
    lab.place(x=170,y=315)
    mainf2.pack(fill=BOTH,expand=1)
    dt=var.get()
    scr.mainloop()

def main():
    scr1=Tk()
    scr1.geometry("700x350")
    scr1.title("Twitter Data Sentiment Analysis")
    scr1.resizable(False, False)
    mainf2=Frame(scr1,height=618,width=1366)
    c=Canvas(mainf2,height=618,width=1366)
    c.pack()
    b=Button(mainf2,height=2,width=12,text='Online',font=('Times New Roman',14,'bold'),bg='green',fg='white',command=lambda :page_three(scr1))
    b.place(x=280,y=100)
    b1=Button(mainf2,height=2,width=12,text='Offline',font=('Times New Roman',14,'bold'),bg='red',fg='white',command=lambda :page_two(scr1))
    b1.place(x=280,y=170)
    back=PhotoImage(file="abc.gif")
    c.create_image(350,172,image=back)
    lab=Label(mainf2,text= "Created by Prabhat Ranjan Dubey",fg="red",font=('Times New Roman',20,'bold'),bg='sky blue')
    lab.place(x=170,y=315)
    mainf2.pack(fill=BOTH,expand=1)
    scr1.mainloop()

def result(scr,p,ne,n):
    scr.destroy()
    root=Tk()
    root.geometry("700x350")
    root.title("Twitter Data Sentiment Analysis")
    root.resizable(False, False)
    mainf2=Frame(root,height=700,width=1366)
    c=Canvas(mainf2,height=618,width=1366,bg='white')
    c.pack()
    img=ImageTk.PhotoImage(Image.open("smiley.jpg"),width=900)
    c.create_image(350,172,image=img)
    lab=Label(mainf2,text="Postitive\n   "+str(p)+"%",font=('Times New Roman',12,'bold'),bg='white')
    lab.place(x=80,y=270)
    lab1=Label(mainf2,text="Neutral\n   "+str(ne)+"%",font=('Times New Roman',12,'bold'),bg='white')
    lab1.place(x=260,y=270)
    lab2=Label(mainf2,text="Negative\n   "+str(n)+"%",font=('Times New Roman',12,'bold'),bg='white')
    lab2.place(x=460,y=270)
    mainf2.pack(fill=BOTH,expand=1)
    

    d=[p,ne,n]
    l=['Positive','Neutral','Negative']

   
    p=plt.subplot(1,2,1)
    p.pie(d,labels=l,autopct="%0.2f",shadow=True,explode=(0.1,0,0),colors=['green','blue','red'])
    #p.title("Sentiment Analysis on PM Narendra Modi's Tweets")
    plt.title("Twitter Data Sentiment Analysis",size=20)
    p1=plt.subplot(1,2,2)
    p1.bar(l,d,color=['green','blue','red'])
    #p1.title("Sentiment Analysis on PM Narendra Modi's Tweets")
    #p1.ylabels("Sentiments in %")
    
    plt.show()

    
main()




   
