
bookIndexMap={}
userIndexMap={}

def reindex():
    userIndex=0
    bookIndex=0
    ratingLimit=50000
    N=1
    with open('book rating.txt') as F,open('bookMap.txt','w') as F1, open('userMap.txt','w') as F2, open('BookDataSet.txt','w') as F3:
        lines=F.readlines()
        for line in lines[1:]:
            user,isbn,rate=line.strip('\n').split(';')
            u= user.strip('"')
            i=isbn.strip('"')
            r=int(rate.strip('""'))



            if not bookIndexMap.keys().__contains__(i):
                bookIndexMap[i]=bookIndex
                F1.write(str(i)+' '+str(bookIndex)+'\n')
                bookIndex+=1
            if not userIndexMap.keys().__contains__(u):
                userIndexMap[u]=userIndex
                F1.write(str(u)+' '+str(userIndex)+'\n')
                userIndex+=1
            if r==0:
                print 'rating 0\n'
                continue
            line=str(userIndexMap[u])+' '+str(bookIndexMap[i])+' '+str(r)+'\n'
            F3.write(line)
            print line
            N+=1
            if N>=ratingLimit:
                break

    with open('log.txt','w') as G:
        G.write(str(N)+' '+str(userIndex)+' '+str(bookIndex))



            #print user.strip('"'),isbn.strip('"'),)




if __name__ == '__main__':
    reindex()