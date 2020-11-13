import mysql.connector
import time
import sys
import os
from datetime import date
from clear import clear
from loading import loadFast,loadClean

CURSOR_UP_ONE = '\x1b[1A' 
ERASE_LINE = '\x1b[2K' 


db=mysql.connector.connect(host="localhost",user="root",passwd="root",port="3307")
mycursor=db.cursor()

def refresh(db,mycursor):
    db.close()
    mycursor.close()
    db1=mysql.connector.connect(host="localhost",user="root",passwd="root",port="3307")
    mycursor1=db1.cursor()
    return db1,mycursor1

'''FUNCTIONS'''

def shopList():
    shops=[]
    mycursor.execute("Show databases")
    temp=mycursor.fetchall()
    for x in temp:
        y=''.join(x)
        shops.append(y)
    return shops

def createShop():
    name="mysql"
    flag="NO"
    while name in shops and flag!="YES":
        clear()
        loadClean(25,0.004)
        print("===================CREATE A SHOP==================\n")
        name=input("Enter the name of the shop:")
        if name in shops:
            print("The name you entered for the shop is already taken.Please try something else\n")
            time.sleep(3)
            flag=input("TYPE 'YES' TO EXIT AND GO BACK ELSE PRESS ENTER.")
        else:
            print("Perfect Choice.\n")

    if flag=="YES" :
        return
    mycursor.execute("Create database "+name)
    
    admin=input("Enter the name of the admin:")
    adminpass=input("\nEnter the password for the admin:")
    print("\n\nThe new shop is being created...\n")
    for x in range (0,7):  
        b = "Loading" + "." * x
        print (b, end="\r")
        time.sleep(0.4)

    
    balance=input("Enter the account balance for your shop's bank account\n")
    mycursor.execute("use "+name)
    mycursor.execute("create table shopInfo(title varchar(255),storedNum int(255),storedChar varchar(255))")
    
    mycursor.execute("insert into shopInfo values('empNo',0,'NULL')")
    mycursor.execute("insert into shopInfo values('balance',"+balance+",'NULL')")
    mycursor.execute("insert into shopInfo values('transNo',0,'NULL')")
    mycursor.execute("insert into shopInfo values('OrderNo',0,'NULL')")
    mycursor.execute("insert into shopInfo values('StoreOrderNo',0,'NULL')")
    
    mycursor.execute("create table transactions(transNo int(5),orderNo int(5),itemName varchar(255),amount int(5),quantity int(5),status varchar(255))")
    mycursor.execute("create table orders(orderNo int(5),shopname varchar(255),orderdate date,transTotal int(5),amount int(5))")
    mycursor.execute("create table employeeList ( employeeId int(5), employeeName varchar(255), username varchar(255),password varchar(255))")
    mycursor.execute("create table inventory (itemId int(5),itemName varchar(255),quantity int(5),price int(10))")
    mycursor.execute("create table shopOrder (transId int(5),itemId int(5),quantity int(10),price int(5),cost int(5),orderdate date,status varchar(255),placedby varchar(255))")
    mycursor.execute("create table hub (itemId int(5),itemName varchar(255),price int(5))")

    cd="insert into employeeList (employeeId,employeeName,username,password) values (%s,%s,%s,%s)"
    admininfo=(0,"admin",admin,adminpass)
    mycursor.execute(cd,admininfo)

    sql = "INSERT INTO hub (itemId,itemName,price) VALUES (%s, %s,%s)"
    val = [
    ('1', 'book',10),
    ('2', 'pen',100),
    ('3', 'paper',150),
    ('4', 'clips',30),
    ('5', 'glue',5),
    ('6', 'gel pen',200),
    ('7', 'ball pen',30),
    ('8', 'pencil',15),
    ('9', 'eraser',18),
    ('10', 'register',36),
    ('11', 'notebook',86),
    ('12', 'fountain pen',87),
    ('13', 'dictionary',33),
    ('14', 'drawing book',29),
    ('15', 'crayons',45),
    ('16', 'pencil colours',70),
    ('17', 'ruler',200),
    ('18', 'divider',163),
    ('19', 'set squares',2),
    ('20', 'chips',1),
    ]

    mycursor.executemany(sql, val)
    
    print("Making Necessary databases\n")

    for i in range(0,5):
        temp="["
        temp1='@'*(i*2)
        temp2='.'*(10-(i*2))
        temp=temp+temp1
        temp=temp+temp2
        temp+=']'
        print(temp, end='\r', flush=True)
        time.sleep(0.5)
        sys.stdout.flush()

    print("THE ACCOUNT HAS BEEN CREATED.\n")
    input("Press Enter to continue....")

    print("The program will exit now.Restart to use the recently created database")

    db.commit()
    clear()

def makeSale():
    clear()
    loadClean(25,0.004)
    mycursor.execute("select * from shopinfo where title='orderNo'")
    orderNo=mycursor.fetchall()
    mycursor.execute("update shopinfo set storedNum=storedNum+1 where title='orderNo'")
    swit="YES"
    mycursor.execute("select storedNum from shopinfo where title='transNo'")
    trans=mycursor.fetchall()
    tran=int(trans[0][0])
    mycursor.execute("select storedNum from shopinfo where title='orderNo'")
    orders=mycursor.fetchall()
    ordr=int(orders[0][0])
    totaltrans=0
    amount=0
    while swit=="YES" :
        tran+=1
        totaltrans+=1
        mycursor.execute("select * from inventory")
        inventoryList=mycursor.fetchall()
        for x in inventoryList:
            print("Item ID:"+str(x[0])+"  ItemName:"+str(x[1])+"  ItemQuantity:"+str(x[2])+"  ItemPrice:"+str(x[3]))
        if len(inventoryList)==0:
            print("There is no item in the inventory")
            for x in range (0,7):  
                b = "Going Back." + "." * x
                print (b, end="\r")
                time.sleep(0.4)
            return
        x=int(input("Enter the object id:"))
        param=(x,)
        quer="select * from inventory where itemId=%s"
        mycursor.execute(quer,param)
        num=mycursor.fetchall()
        if len(num)==0:
            print("No iteams with such an ID exists.Please recheck your ID")
            totaltrans-=1
            tran-=1
            continue
        quan=int(input("Enter the quantity that you for sale:"))
        if(quan<num[0][2]):
            bal=num[0][3]*quan
            amount+=bal
            rem=num[0][2]-quan
            q1="update shopinfo set storedNum=storedNum+%s where title='balance'"
            q2=(bal,)
            mycursor.execute(q1,q2)
            q1="update inventory set quantity=%s where itemId=%s"
            q2=(rem,num[0][0],)
            mycursor.execute(q1,q2)
            q1="insert into transactions values(%s,%s,%s,%s,%s,%s)"
            q2=(tran,ordr,num[0][1],bal,quan,"SUCCESSFUL",)
            mycursor.execute(q1,q2)
            print("Transactions successful!")
        elif quan==num[0][2]:
            bal=num[0][3]*quan
            amount+=bal
            q1="update shopinfo set storedNum=storedNum+%s where title='balance'"
            q2=(bal,)
            mycursor.execute(q1,q2)

            q1="insert into transactions values(%s,%s,%s,%s,%s,%s)"
            q2=(tran,ordr,num[0][1],bal,quan,"SUCCESSFUL")
            mycursor.execute(q1,q2)

            q1="delete from inventory where itemId=%s"
            q2=(num[0][0],)
            mycursor.execute(q1,q2)
            print("Transactions Successful.No more items of id "+str(num[0][0])+" remaining.")
        else:
            q1="insert into transactions values(%s,%s,%s,%s,%s,%s)"
            q2=(tran,ordr,num[0][1],num[0][3]*quan,quan,"FAILED!!")
            mycursor.execute(q1,q2)
            print("The quantity that you entered is more than inventory.\nTRANSACTION CANCELLED.")
        swit=input("Type YES to Add more Items to Order...\n")
    q1="update shopinfo set storedNum=%s where title='transno'"
    q2=(tran,)
    mycursor.execute(q1,q2)
    q1="update shopinfo set storedNum=%s where title='orderno'"
    q2=(ordr,)
    mycursor.execute(q1,q2)
    q1="insert into orders values(%s,%s,%s,%s,%s)"
    q2=(ordr,shopname,day,totaltrans,amount,)
    mycursor.execute(q1,q2)
    print("ORDER ID "+str(ordr)+" has successfully been updated.")
    db.commit()

def viewInventory():
    clear()
    loadClean(25,0.004)
    print("=============INVENTORY=============")
    mycursor.execute("select * from inventory")
    inv=mycursor.fetchall()
    print("The list of the items is:")
    items=[]
    for x in inv:
        print("ItemId: "+str(x[0])+"  ItemName: "+str(x[1])+"  ItemQuantity: "+str(x[2])+"  ItemPrice:"+str(x[3]))
        items.append(int(x[0]))
    
    if len(inv)==0:
        print("The inventory in empty")
        loadFast(5,0.5)
        return
    else:
        print("The total number of items is "+str(len(inv)))
        loadFast(5,0.5)
    
    print("========UPDATE PRICE========")
    print("1.Update price")
    print("2.Go bacK")
    choice=int(input("Enter your choice:"))
    if(choice==1):
        itemNum=-1
        while itemNum not in items:
            itemNum=int(input("Input the item number:"))
            if itemNum not in items:
                print("The items is not present in the invenotory.Try again")
        price=int(input("Enter the updated price of the item."))
        mycursor.execute("select * from inventory where itemId="+str(itemNum))
        temp=mycursor.fetchall()
        dx="update inventory set price=%s where ItemId=%s"
        dy=(price,itemNum,)
        mycursor.execute(dx,dy)
        print("The price of {} with itemid {} has been updated from {} to {}.".format(temp[0][1],temp[0][0],temp[0][3],price))
        db.commit()
        input("Press Enter to continue.")
    else:
        print("Going Back....")
        loadClean(20,0.04)
        return
    


def viewAccountBalance():
    clear()
    loadClean(25,0.004)
    print("===========BALANCE===========")
    mycursor.execute("select * from shopInfo where title='balance'")
    bal=mycursor.fetchall()
    print("The balance of the shop accounts is {}".format(bal[0][1]))
    input("Press enter to continue......\n") 

def customerOrderHistory():
    choice2=-1
    while(choice2!=5):
        clear()
        loadClean(25,0.004)
        print("============Order info MENU===============")
        print("1.Past orders in ascending order")
        print("2.Past orders in descending order")
        print("3.Info for a particular order")
        print("4.List out all orders")
        print("5.Go back")
        choice2=int(input("Enter your choice:"))
        if choice2==1:
            mun=int(input("Enter the number of records(From Start):"))
            q1="select * from (select * from orders order by orderNo asc) as T limit %s"
            q2=(mun,)
            mycursor.execute(q1,q2)
            temp=mycursor.fetchall()
            cnt=0
            for x in temp:
                print(str(cnt)+".")
                cnt+=1
                print("OrderNo:{}  Shopname:{}  Orderdate:{}  Totaltrans:{}  amount:{}".format(x[0],x[1],x[2],x[3],x[4]))
            input("Press Enter to continue....")
        
        elif choice2==2:
            mun=int(input("Enter the number of records(From Last):"))
            q1="select * from (select * from orders order by orderNo desc) as T limit %s"
            q2=(mun,)
            mycursor.execute(q1,q2)
            temp=mycursor.fetchall()
            cnt=1
            for x in temp:
                print(str(cnt)+".")
                cnt+=1
                print("OrderNo:{}  Shopname:{}  Orderdate:{}  Totaltrans:{}  amount:{}".format(x[0],x[1],x[2],x[3],x[4]))
            input("Press Enter to continue....")
        
        elif choice2==3:
            x=int(input("Enter the order number that you want to look for:"))
            q1="select * from orders where orderNo=%s"
            q2=(x,)
            mycursor.execute(q1,q2)
            trans=mycursor.fetchall()
            if len(trans)==0:
                print("Invalid order no.")
            else:
                for x in trans:
                    print("OrderNo:{}  Shopname:{}  Orderdate:{}  Totaltrans:{}  amount:{}".format(x[0],x[1],x[2],x[3],x[4]))
            input("Press Enter key to continue......")
        
        elif choice2==4:
            mycursor.execute("select * from orders")
            temp=mycursor.fetchall()
            for x in temp:
                print("OrderNo:{}  Shopname:{}  Orderdate:{}  Totaltrans:{}  amount:{}".format(x[0],x[1],x[2],x[3],x[4]))
            input("Press Enter key to continue......")
        
        elif choice2==5:
            print("Going Back...")
            break
        else:
            print("Please enter the correct choice.You have entered invalid input.")
            input("Press Enter key to continue")

def customerTransactionHistory():
    choice2=-1
    while(choice2!=5):
        clear()
        loadClean(25,0.004)
        print("============TRANSACTION info MENU===============")
        print("1.Oldest Transactions")
        print("2.Latest Transactions")
        print("3.Info for a particular transaction")
        print("4.List out all transactions")
        print("5.Go back")
        choice2=int(input("Enter your choice:"))
        if choice2==1:
            mun=int(input("Enter the number of records(From Start):"))
            q1="select * from (select * from transactions order by transno asc) as T limit %s"
            q2=(mun,)
            mycursor.execute(q1,q2)
            temp=mycursor.fetchall()
            cnt=0
            for x in temp:
                print(str(cnt)+".")
                cnt+=1
                print("TransNo:{}  OrderNo:{}  ItemName:{} Amount:{} Quantity:{}  Status:{}".format(x[0],x[1],x[2],x[3],x[4],x[5]))
            input("Press Enter to continue....")
        
        elif choice2==2:
            mun=int(input("Enter the number of records(From Last):"))
            q1="select * from (select * from transactions order by transno desc) as T limit %s"
            q2=(mun,)
            mycursor.execute(q1,q2)
            temp=mycursor.fetchall()
            cnt=1
            for x in temp:
                print(str(cnt)+".")
                cnt+=1
                print("TransNo:{}  OrderNo:{}  ItemName:{} Amount:{} Quantity:{}  Status:{}".format(x[0],x[1],x[2],x[3],x[4],x[5]))
            input("Press Enter to continue....")
        
        elif choice2==3:
            x=int(input("Enter the transaction number that you want to look for:"))
            q1="select * from transactions where transno=%s"
            q2=(x,)
            mycursor.execute(q1,q2)
            trans=mycursor.fetchall()
            if len(trans)==0:
                print("Invalid transaction no.")
            else:
                for x in trans:
                    print("TransNo:{}  OrderNo:{}  ItemName:{} Amount:{} Quantity:{}  Status:{}".format(x[0],x[1],x[2],x[3],x[4],x[5]))
            input("Press Enter key to continue......")
        
        elif choice2==4:
            mycursor.execute("select * from transactions")
            temp=mycursor.fetchall()
            for x in temp:
                print("TransNo:{}  OrderNo:{}  ItemName:{} Amount:{} Quantity:{}  Status:{}".format(x[0],x[1],x[2],x[3],x[4],x[5]))
            input("Press Enter key to continue......")
        
        elif choice2==5:
            print("Going Back...")
            break
        else:
            print("Please enter the correct choice.You have entered invalid input.")
            input("Press any key to continue")

def shopOrderHistory():
    choice2=-1
    while(choice2!=5):
        clear()
        loadClean(25,0.004)
        print("============Shop's Orders info MENU===============                     "+"ADMIN MODE")
        print("1.Oldest Orders")
        print("2.Latest Orders")
        print("3.Look for a particular order")
        print("4.List out all orders")
        print("5.Back")
        choice2=int(input("Enter your choice:"))
        if choice2==1:
            mun=int(input("Enter the number of records(From Start):"))
            q1="select * from (select * from shoporder order by transid asc) as T limit %s"
            q2=(mun,)
            mycursor.execute(q1,q2)
            temp=mycursor.fetchall()
            cnt=0
            for x in temp:
                cnt+=1
                print(str(cnt)+".")
                print("OrderID:{}  ItemID:{}  quantity:{}  Price/Piece:{}  TotalCost:{}  OrderDate:{} Status:{}".format(x[0],x[1],x[2],x[3],x[4],x[5],x[6]))
            input("Press Enter to continue....")
        
        elif choice2==2:
            mun=int(input("Enter the number of records(From Last):"))
            q1="select * from (select * from shoporder order by transid desc) as T limit %s"
            q2=(mun,)
            mycursor.execute(q1,q2)
            temp=mycursor.fetchall()
            cnt=1
            for x in temp:
                print(str(cnt)+".")
                cnt+=1
                print("OrderID:{}  ItemID:{}  quantity:{}  Price/Piece:{}  TotalCost:{}  OrderDate:{} Status:{}".format(x[0],x[1],x[2],x[3],x[4],x[5],x[6]))
            input("Press Enter to continue....")
        
        elif choice2==3:
            x=int(input("Enter the Order number that you want to look for:"))
            q1="select * from shoporder where transid=%s"
            q2=(x,)
            mycursor.execute(q1,q2)
            trans=mycursor.fetchall()
            if len(trans)==0:
                print("Invalid ShopOrder no.")
            else:
                for x in trans:
                        print("OrderID:{}  ItemID:{}  quantity:{}  Price/Piece:{}  TotalCost:{}  OrderDate:{} Status:{}".format(x[0],x[1],x[2],x[3],x[4],x[5],x[6]))
            input("Press Enter key to continue......")
        
        elif choice2==4:
            mycursor.execute("select * from shoporder")
            temp=mycursor.fetchall()
            for x in temp:
                print("OrderID:{}  ItemID:{}  quantity:{}  Price/Piece:{}  TotalCost:{}  OrderDate:{} Status:{}".format(x[0],x[1],x[2],x[3],x[4],x[5],x[6]))
            use=input("Press any key to continue......")
        
        elif choice2==5:
            print("Going Back...")
            break
        else:
            print("Please enter the correct choice.You have entered invalid input.")
            use=input("Press any key to continue")

def placeInventoryOrdersAdmin(usrname):
    clear()
    loadClean(25,0.004)
    mycursor.execute("select * from hub")
    hublist=mycursor.fetchall()
    Items=[]
    mycursor.execute("select * from shopinfo where title='storeorderno'")
    indexx=mycursor.fetchall()
    index=int(indexx[0][1])
    for x in hublist:
        print("ItemId:"+str(x[0])+"  ItemName:"+str(x[1])+"  ItemPrice:"+str(x[2]))
        Items.append(x[0])
    ch=-1
    price=[]
    print()
    while ch not in Items:
        ch=int(input("Enter the ID of the element of your choice."))
        if ch not in Items:
            print("The item that you have entered is not in the list.")
        else:
            temp=(ch,)
            q1="select * from hub where itemId=%s"
            mycursor.execute(q1,temp)
            price=mycursor.fetchall()
    num=int(input("Enter the total number of items that you want: "))
    cost=num*price[0][2]
    print("Cost will be "+str(cost))
    mycursor.execute("select storedNum from shopinfo where title='balance'")
    bal=mycursor.fetchall()
    if bal[0][0]<cost:
        print("INSUFFICIENT BALANCE.TRY AGAIN LATER")
        input("Press Enter key to continue..")
        return
    
    q1="update shopinfo set storedNum=%s where title='balance'"
    newval=bal[0][0]-cost
    q2=(newval,)
    mycursor.execute(q1,q2)
    q1="select * from inventory where itemid=%s"
    s1=(ch,)
    mycursor.execute(q1,s1)
    cur=mycursor.fetchall()
    SP=int(input("Enter the selling price that you would like to list the product at:"))
    if(len(cur)==0):
        last=(price[0][0],price[0][1],num,SP)
        q2="insert into inventory values(%s,%s,%s,%s)"
        mycursor.execute(q2,last)
    else:
        ttl=cur[0][2]+num
        last=(ttl,ch)
        q2="update inventory set quantity=%s where itemid=%s"
        mycursor.execute(q2,last)
    q1="insert into shoporder values(%s,%s,%s,%s,%s,%s,%s,%s)"
    index+=1
    q2=(index,ch,num,price[0][2],price[0][2]*num,day,"COMPLETED","admin/"+str(usrname))
    mycursor.execute(q1,q2)
    q1="update shopinfo set storedNum=%s where title='storeorderno'"
    q2=(index,)
    mycursor.execute(q1,q2)
    print("The order has been placed and the databases have been updated.")
    db.commit()
    input("Enter Enter to continue...")
    return

def approveOrders():
    choice=1
    clear()
    loadClean(25,0.004)
    mycursor.execute("select * from shopOrder where status='PENDING'")
    temp=mycursor.fetchall()
    print("You have {} pending orders to approve. ".format(len(temp)))
    if(len(temp)==0):
        input("No pending orders.Press Enter to continue...")
        return
    OrderNo=[]
    for x in temp:
        print("OrderId: {}  ItemID: {} Quantity: {} ItemPrice: {}  TotalCost: {} OrderDate:{} Status: {} PlacedBy:{} ".format(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]))
        OrderNo.append(int(x[0]))
        
    print()
    inp=int(input("Enter the order number that you want to choose:"))
    if inp not in OrderNo:
        print("The OrderNo entered by you isnt pending.")
        input("Press Enter to continue")
        return
    else:
        choice=1
        while choice!=3:    
            clear()

            print("==============APPROVE/CANCEL Order - {} ================".format(inp))
            print("1.Approve the selected Order")
            print("2.Cancel the selected Order")
            print("3.Go back")
            choice=int(input("Enter your choice"))
            if choice==1:
                mycursor.execute("select * from shopOrder where transId="+str(inp))
                x=mycursor.fetchall()
                cost=int(x[0][4]) 
                mycursor.execute("select storedNum from shopinfo where title='balance'")
                bal=mycursor.fetchall()
                if cost>bal[0][0]:
                    print("INSUFFICIENT FUNDS.CANT COMPLETE TRANSACTION")
                    input("Press Enter to continue")
                    return
                else:
                    q1="update shopinfo set storedNum=%s where title='balance'"
                    newval=bal[0][0]-cost
                    q2=(newval,)
                    mycursor.execute(q1,q2)
                    q1="select * from inventory where itemid=%s"
                    s1=(x[0][1],)
                    mycursor.execute(q1,s1)
                    cur=mycursor.fetchall()
                    mycursor.execute("select * from hub where itemId="+str(x[0][1]))
                    name=mycursor.fetchall()
                    SP=int(input("Enter the selling price that you would like to list the product at:"))
                    if(len(cur)==0):
                        last=(x[0][1],name[0][1],x[0][2],SP)
                        q2="insert into inventory values(%s,%s,%s,%s)"
                        mycursor.execute(q2,last)
                    else:
                        ttl=cur[0][2]+x[0][2]
                        last=(ttl,x[0][1])
                        q2="update inventory set quantity=%s where itemid=%s"
                        mycursor.execute(q2,last)
                
                mycursor.execute("update shopOrder set status='COMPLETED' where transId="+str(inp))
                print("The Order has been successfully Completed")
                input("Press Enter to continue.")
                choice=3

            elif choice==2:
                mycursor.execute("update shopOrder set status='CANCELLED' where transId="+str(inp))
                print("OrderID:{} has been cancelled indefinitely.".format(inp))
                input("Press Enter to Continue")
                choice=3
            elif choice==3:
                print("Going Back..")
                time.sleep(2)
            
            else:
                print("You have entered the wrong choice.Please enter the right choice.")
            db.commit()
        

def placeInventoryOrdersEmployee(usrname):
    clear()
    loadClean(25,0.004)
    mycursor.execute("select * from hub")
    hublist=mycursor.fetchall()
    Items=[]
    mycursor.execute("select * from shopinfo where title='storeorderno'")
    indexx=mycursor.fetchall()
    index=int(indexx[0][1])
    for x in hublist:
        print("ItemId:"+str(x[0])+"  ItemName:"+str(x[1])+"  ItemPrice:"+str(x[2]))
        Items.append(x[0])
    ch=-1
    price=[]
    while ch not in Items:
        ch=int(input("Enter the ID of the element of your choice."))
        if ch not in Items:
            print("The item that you have entered is not in the list.")
        else:
            temp=(ch,)
            q1="select * from hub where itemId=%s"
            mycursor.execute(q1,temp)
            price=mycursor.fetchall()
    num=int(input("Enter the total number of items that you want"))
    cost=num*price[0][2]
    print("Cost will be "+str(cost))
    q1="insert into shoporder values(%s,%s,%s,%s,%s,%s,%s,%s)"
    index+=1
    q2=(index,ch,num,price[0][2],price[0][2]*num,day,"PENDING","emp/"+str(usrname))
    mycursor.execute(q1,q2)
    q1="update shopinfo set storedNum=%s where title='storeorderno'"
    q2=(index,)
    mycursor.execute(q1,q2)
    print("The order has been placed and the databases have been updated.")
    db.commit()
    input("Enter Enter to continue...")
    return

def hireAndFire():
    choice2=100
    while(choice2 != 4):
        clear()
        loadClean(25,0.004)
        clear()
        print("============== HIRE & FIRE =================")
        print("1.Hire")
        print("2.Fire")
        print("3.Employee List")
        print("4.Go Back")
        cho=int(input("Enter your choice:"))
        if cho==1:
            clear()
            print("********HIRE MENU*********")
            us=input("Enter employee username:")
            ps=input("Enter employee password:")
            mycursor.execute("select storedNum from shopinfo where title='empNo'")
            value=mycursor.fetchall()
            q1="update shopinfo set storedNum=%s where title='empNo'"
            val=value[0][0]+1
            temp=(val,"employee",us,ps,)
            cmd="insert into employeeList values(%s,%s,%s,%s)"
            mycursor.execute(cmd,temp)
            temp=(val,)
            mycursor.execute(q1,temp)
            print("New Employee with username {} has been added to the database.".format(us))
            input("Press Enter to continue..")
            db.commit()
        elif cho==2:
            clear()
            print("********FIRE MENU*********")
            id=0
            while id==0:
                id=int(input("Enter the id of the employee that you wanna fire:"))
                if id==0:
                    print("0 is admins id and admin cant be deleted.Choose again.")
            q1="select * from employeelist where employeeid=%s"
            par=(id,)
            mycursor.execute(q1,par)
            temp=mycursor.fetchall()
            if(len(temp)==0):
                print("No employee with the given ID.CANT DELETE.")
                continue
            q1="delete from employeelist where employeeid=%s"
            mycursor.execute(q1,par)
            print("The employee with ID "+str(id)+" has been deleted successfully.")
            input("Press Enter to continue.....")
            db.commit()
        elif cho==3:
            mycursor.execute("select * from employeelist")
            emp=mycursor.fetchall()
            print("The list of all users is:")
            for x in emp:
                print("UserId:{}  UserType:{}  Username:{}".format(x[0],x[1],x[2]))

            input("Press Enter to continue.")
        elif cho==4:
            break
        else:
            print("You have entered the wrong choice try again.")
            time.sleep(2)

def shutShop():
    x=input("Are you sure that you want to shut down the shop completely?Type YES or NO.\n")
    if x=="YES":
        mycursor.execute("drop database "+ shopname)
        for x in range (0,8):  
            b = "Deleting" + "." * x
            print (b, end="\r")
            time.sleep(0.4)
        print(shopname+" shop has been deleted.Thanks for using our service")
        db.commit()
        input("Press Enter to continue..")
        return True

    
'''Choice variable will be used to switch operations'''
choice=10

#MAIN MENU PYTHON CODE
shutShopCheck=False
while(choice):
    clear()
    '''Selecing and inserting the names of all the shops into the shops array'''
    shops=shopList()
    today=date.today()
    day=today.strftime("%Y-%m-%d")
    db,mycursor=refresh(db,mycursor)
    print("WELCOME TO INVENTORY MANAGEMENT SYSTEM\n")
    print("1.Create a New Shop\n")
    print("2.Login into your Existing Shop\n")
    print("3.Exit\n")
    choice=int(input("Enter your choice here:"))
    print("\n")
    if choice==1:
        createShop()
    
    elif choice==2:
        round=1
        
        while(round):
            clear()
            print("==============WELCOME TO LOGIN MENU==============\n")
            shopname="sdfasdjklghajskghasjlghasjklghasjgdhgkhdasdghkjlasglkasjlgasdjlgjsladghsjaklghasklgaslgsalg"
            emExit=False
            while shopname not in shops:
                shopname=input("Enter the name of your shop:")
                if shopname not in shops:
                    print("The shopname entered by you wasnt found.Please try again.\n")
                    temp=input("Type YES to go back.Press Enter to input another shopname.")
                    if temp=="YES":
                        emExit=True
                if(emExit):
                    break
                
            if(emExit):
                break
            usrname=input("Enter your username:")
            psword=input("Enter your password:")
            
            mycursor.execute("use "+shopname)
            mycursor.execute("select * from employeelist")
            myresult=mycursor.fetchall()
            
            if(len(myresult)==0):
                print("\nThe username or password entered by you is wrong.Please try again.")
                input("Press Enter to continue.")
                continue
            answer=()
            flag=False
            for x in myresult:
                if(x[2]==usrname and x[3]==psword):
                    answer=x
                    flag=True
                    break
            if flag==False:
                print("Username/Password is wrong.")
                use=input("Press Enter key to continue...")
                continue
            
            choice1=100
            
            while(choice1!=10):
                clear()
                print("\nWelcome "+answer[1])
                print("==============ADMIN MENU==============\n")
                if(answer[1]=='admin'):
                
                    print("1.Make a sale")
                    print("2.Check Inventory")
                    print("3.Check Account Balance")
                    print("4.Customer Order History")
                    print("5.Transaction History")
                    print("6.Place orders for more Inventory")
                    print("7.Hire and Fire Employees")
                    print("8.Store Order History")
                    print("9.Shut Shop")
                    print("0.Go back")
                    
                    choice1=int(input("Enter your choice:"))
                    print("")
                    if choice1==1:
                        
                        '''CALLING THE MAKE SALE FUNCTION HERE'''
                        makeSale()
                           
                    elif choice1==2:
                        '''CALLING VIEWACCOUNTBALANCE FUNCTION HERE'''
                        viewInventory()
                    
                    elif choice1==3:
                        '''CALLING VIEWACCOUNTBALANCE FUNCTION HERE'''
                        viewAccountBalance()
                    
                    elif choice1==4:
                        '''CALLING CUSTOMERORDERHISTORY FUNCTION HERE'''
                        customerOrderHistory()

                    elif choice1==5:
                        '''CALLING CUSTOMERTRANSACTIONHISTORY FUNCTION HERE'''
                        customerTransactionHistory()
                    
                    elif choice1==6:
                        '''CALLING PLACEINVENTORYORDERS FUNCTION HERE'''
                        choice3=1
                        while(choice3!=3):
                            clear()
                            print("=======Place Orders for Inventory=========")
                            print("1.Make a new order yourself")
                            print("2.Clear pending employee orders")
                            print("3.Go back")
                            choice3=int(input("Enter your choice:"))
                            if choice3==1:
                                placeInventoryOrdersAdmin(usrname)
                            elif choice3==2:
                                approveOrders()
                            elif choice3==3:
                                print("Going Back...")
                                time.sleep(2)
                                break
                            else:
                                print("Wrong choice.Enter the correct option")
                        
                    elif choice1==7:
                        '''CALLING HIREANDFIRE FUNCTION HERE'''
                        hireAndFire()

                    elif choice1==8:
                        '''CALLING SHOPORDERHISTORY FUNCTION HERE'''
                        shopOrderHistory()


                    elif choice1==9:
                        shutShopCheck=shutShop()

                    
                    elif choice1==0:
                        print("\nGOING BACK....")
                        time.sleep(2)
                        choice1=10
                    else:
                        print("You have entered the wrong choice.Please try again later")
                    
                    if(shutShopCheck):
                        break
                
                else:
                    clear()
                    print("\nWelcome "+answer[2])
                    print("==============EMPLOYEE MENU==============\n")
                    print("1.Make a sale")
                    print("2.Check Inventory")
                    print("3.Customer Order History")
                    print("4.Transaction History")
                    print("5.Place orders for more Inventory")
                    print("6.Store Order History")
                    print("0.Go back")
                    choice1=int(input("Enter your choice:"))

                    print("")
                    
                    if choice1==1:
                        '''Calling the makeSale function to make  sale'''
                        makeSale()
                           
                    elif choice1==2:
                        '''CALLING VIEWACCOUNTBALANCE FUNCTION HERE'''
                        viewInventory()
                    
                    elif choice1==3:
                        customerOrderHistory()

                    elif choice1==4:
                        customerTransactionHistory()
                    
                    elif choice1==5:
                        placeInventoryOrdersEmployee(usrname)

                    elif choice1==6:
                        shopOrderHistory()

                    elif choice1==0:
                        print("\nGOING BACK....")
                        time.sleep(2)
                        choice1=10
                    
                    else:
                        print("You have entered the wrong choice.Please try again later")
            if(shutShopCheck):
                break

    
    elif choice==3:
        for x in range (0,3):  
            b = "Exiting in " + str(3-x)+ " seconds."
            print (b, end="\r")
            time.sleep(1)
        sys.exit(0)   
    
    else:
        print("You chose the wrong option.Please enter the right input\n")
        
        
    



