import pickle
from recommendation import load_object
import numpy as np

'''

User Ui is interested in a item Vj and rated it with Rij stars
therefore, items with rating >= (Rij-th) will be feltched as recommendation.

THe questions that I am interested to answer are:
    1. Give me top 10 similar items to item j
    2. Give me top 10 similar users who bought this rated this item higher than threshold(2)
    3. Give me top 10  similar item that is rated high by this user
    4. Give me users like the current user i


'''
#########Activate following block for MovieLense#############
#W=load_object('Results/test_W')
#H=load_object('Results/test_H')
#############################################


#########Threshold for MovieLens ##############################
#MIN_SIM=0.5   #cosine of 45degree
#MIN_RATE=50
##########################################################

############Activate for Artist dataset#########################
W=load_object('Results/artist_W')
H=load_object('Results/artist_H')
#print W.shape, H.shape
################## for Artist Threshold###################################

MIN_SIM=0.5   #cosine of 45degree
MIN_RATE=50
#########################################################################

itemDic={}



#print W[u,:]
#print H[:,i]
#v=np.array()

def rating(user,item):

    rate=np.dot(W[user],H[:,item])
    #print 'users Predicted Rate for item i is:', rate
    return rate
############User similarities#################333
def topusers(user,min_sim=MIN_SIM):
    '''
    Find the top similar user for the given user based on cosine similarity in Latent Space
    :param user: UserID
    :param min_sim: Threshold Similarity value
    :return: List of Similar users sorted in descending order based on Similarity Measure
    '''
    print 'Finding Similar Users\n'
    sim_users=[]
    v1=np.array(W[user])
    for i in range(W.shape[0]):
        if i==user:
            continue
        v2=np.array(W[i].transpose())
        dot_mul=np.dot(v1,v2)
        norm=np.linalg.norm(v1)*np.linalg.norm(v2),
        sim=dot_mul/norm
        sim=sim[0][0]
        if sim>=min_sim:
            sim_users.append((i,sim))

    return sorted(sim_users,key=lambda x:x[1],reverse=True)

############################33
def topitems(item, min_sim=MIN_SIM):
    '''
    Find the top similar Items for the given Item based on cosine similarity in Latent Space
    :param item: ItemID
    :param min_sim: Threshold Similarity Value
    :return: List of Similar Items sorted in descending order based on Similarity Measure
    '''
    print 'Finding Item Similarities\n'
    sim_items=[]
    v1=np.array(H[:,item]).transpose()
    for i in range(H.shape[1]):
        if i==item:
            continue
        v2=np.array(H[:,i])
        dot_mul=np.dot(v1,v2)
        norm=np.linalg.norm(v1)*np.linalg.norm(v2),
        sim=dot_mul/norm
        sim=sim[0][0]
        if sim>=min_sim:
            sim_items.append((i,sim))

    return sorted(sim_items,key=lambda x:x[1],reverse=True)

############################################################3

def similarPeopleLikeTheseItems(user):
    '''
    People similar to user also like the following items
    :param user: userID
    :return: list of top rated items
    '''
    ratedItem=[]
    sim_users=topusers(user)
    for u,_ in sim_users:
        for i in range(H.shape[1]):
            rate=rating(u,i)
            if rate>=MIN_RATE:
                ratedItem.append(i)
    return list(set(ratedItem))
def similarPeopleLikeTheseSimilarItems(user,item):
    '''
    people similar to user also liked the following items similar to the Item
    :param user:
    :return:
    '''
    ratedItem=[]
    sim_users=topusers(user)
    sim_items=topitems(item)
    for  u,_ in sim_users:
        for i,_ in sim_items:
            rate_ui=rating(u,i)
            if rate_ui>=MIN_RATE:
                ratedItem.append(i)

    return list(set(ratedItem))

def userAlsoLikeTheseItems(user):
    '''
    Items that this user is interested other than the item
    :param user: UserID
    :return:  toprated Items for this User
    '''
    #V1=np.array(W[user])
    ratedItems=[]
    for i in range(H.shape[1]):
        rate=rating(user,i)
        if rate>=MIN_RATE:
            ratedItems.append((i,rate))
    return sorted(ratedItems,key=lambda x:x[1],reverse=True)

def userLikeTheseSimilarItems(user,item):
    '''
    Items that are similar to item and user likes them
    :param user: User ID
    :param item:  Item ID
    :return: sorted list of items and rate  for which user rated higher
    '''
    ratedItems=[]
    sim_items=topitems(item)
    for i,_ in sim_items:
        rate=rating(user,i)
        if rate>=MIN_RATE:
            ratedItems.append((i,rate))
    return sorted(ratedItems,key=lambda x:x[1],reverse=True)
def topUsersByItem(item):
    '''

    Find the users who rated this items high
    :param item: itemID
    :return: list of user sorted by ratings
    '''
    userbyitem=[]
    for u in range(W.shape[0]):
        rate=rating(u,item)
        if rate>=MIN_RATE:
            userbyitem.append((u,rate))
    return sorted(userbyitem,key=lambda x:x[1],reverse=True)

def peopleLikethisitemAlsoLikeTheseItems(item):

    userbyitem=topUsersByItem(item)
    items=[]
    for u,_ in userbyitem:
        for i in range(H.shape[1]):
            if i==item:
                continue
            rate=rating(u,i)
            if rate>=MIN_RATE:
                items.append(i)
    return list(set(items))

def loadItemsDescription(filename):
    itemDic={}
    for line in open(filename):
        id,name=line.split('|')[0:2]
        itemDic[int(id)]=name
    return itemDic
def load_artist_description(fileName):
    artistDic={}
    for line in open(fileName):
        print line.split()
        tag,name=line.strip('\n').split('\t')
        artistDic[int(tag)]=name
    artistDic[333]='Other'
    return artistDic
def itemLookUp(item):
    return itemDic[item]

def printItems(items):
    for i,_ in items[0:10]:
        print itemLookUp(i+1),'\n'
def itemNames(items):
    for i in items:
        print itemLookUp(i+1)

def writeOutput(user,item,itemFile):
    with open('Results/Artist_recom.txt','w') as F:
        itemDic=load_object(itemFile)
        #print itemDic
        #print'Products simmilar This Item\n'
        F.write("This File contains the details outcomes of several queries\n")
        F.write("Matrix Size:"+str(W.shape[0])+'x'+str(H.shape[1])+" Number of Factors:"+str(W.shape[1])+'\n')
        F.write("############################################################\n")
        F.write("UserId:"+str(user)+'\n')
        F.write("ItemId:"+str(item)+' ItemName:'+itemDic[item+1]+'\n')
        F.write("\n##########Simmialr Items to the given items##########\n")

        items=topitems(item)[1:10]
        print items
        for i,_ in items:
            F.write(str(i)+":"+itemDic[i+1]+"\n")

        F.write("\n##########Users who like this item also like following items##########\n")
        items=peopleLikethisitemAlsoLikeTheseItems(item)[0:10]
        print items
        for i in items:
            F.write(str(i)+":"+itemDic[i+1]+"\n")

        F.write("\n##########Similar Users Like The Following Items##########\n")
        items=similarPeopleLikeTheseItems(user) [1:10]
        print items
        for i in items:
            F.write(str(i)+":"+itemDic[i+1]+"\n")
        F.write("\n##########Similar People like these Items which are similar to the Given Item##########\n")
        items=similarPeopleLikeTheseSimilarItems(user,item)[1:10]
        print items
        for i in items:
            F.write(str(i)+":"+itemDic[i+1]+"\n")
        F.write("\n##########The Given user also rated following items higher than Threshold##########\n")
        items=userAlsoLikeTheseItems(user) [1:10]
        print items
        for i,_ in items:
            F.write(str(i)+":"+itemDic[i+1]+"\n")




if __name__ == '__main__':

    from recommendation import save_object
    user=1
    item=61
    #save_object(load_artist_description('Datasets/Description/tags.dat'),'Datasets/Description/tags')

    #### to run the program for MovieLens Data##########################
    #writeOutput(user,item, 'Datasets/Description/items')
    ###############################################################
    ####################Activate this block to Run the program for Artist Dataset################
    writeOutput(user,item, 'Datasets/Description/tags')
    ###################################################################################

    #print rating(user,item)


