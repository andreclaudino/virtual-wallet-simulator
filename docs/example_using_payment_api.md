
# Stone Payment API example

## Configuration

This notebook is an example of how using stone payment api generated in https://slack-files.com/T06M9ENDT-F5XK4J0P2-532510c5c0

first step is to configure API parameters, in this case, the URL which will be used. For a local API it will be https://0.0.0.0:8080/


```python
url = 'https://0.0.0.0:8080/'
api = lambda s: url+s
```

## Importing necessary libraries


```python
import requests as req
import json
from datetime import datetime
```

## Creating user and get token

Before anything, we need to create an user than get token for access


```python
user_arguments = {
    'name':"Darth Vader",
    'username':"dvader",
    'address':"290, Death Star",
    'phone_number':'+55 21 2265-9865',
    'mail_address':'vader@black_side.com',
    'password':'h@rd_p4ss'}
```


```python
r = req.post(api('user'), data=user_arguments)
user = r.json()
print(user)
```

    {'active': True, 'username': 'dvader', 'wid': 'ac263724cef1492f947fe819df6166f6', 'name': 'Darth Vader', 'uid': 'bf0249caa27f4da8bd2e73496b3e7308', 'mail_address': 'vader@black_side.com'}


once user is created, next step is getting token, this is done with login


```python
r = req.post(api('login'),
             data=dict(username=user_arguments['username'], password=user_arguments['password']))
result = r.json()
```

login return user and token, it is:


```python
print(result['user'])
```

    {'active': True, 'username': 'dvader', 'wid': 'ac263724cef1492f947fe819df6166f6', 'name': 'Darth Vader', 'uid': 'bf0249caa27f4da8bd2e73496b3e7308', 'mail_address': 'vader@black_side.com'}


User object contains the fields send in user creation, and the following ones:

*  wid: user wallet uuid
*  uid: user uuid
*  active: boolean defining when user can login or not


```python
token = result['token']
print(token)
```

    eyJleHAiOjE1MDQwNTEwODAsImFsZyI6IkhTMjU2IiwiaWF0IjoxNTA0MDQ3NDgwfQ.WyJkdmFkZXIiLCJiZjAyNDljYWEyN2Y0ZGE4YmQyZTczNDk2YjNlNzMwOCIsImFjMjYzNzI0Y2VmMTQ5MmY5NDdmZTgxOWRmNjE2NmY2Il0.RPfsotB_v4uCdPiyU4R1j1kCZ6N_v2mQJK25LsVOeHA


token is a cryptographed list with user uid, wallet uid and username. The necessary to perform operations in user and wallet endpoints. Except login and creation, other endpoint calls need token in a header called token.

## Get wallet information

Once we have token, we can get wallet information.

For next uses, I will define a default headers dictionary:


```python
headers = {'token': token}
```


```python
r = req.get(api('wallet'), headers=headers)
wallet = r.json()
```


```python
print(wallet)
```

    {'total_used': 0.0, 'free_limit': 0.0, 'max_limit': 0.0, 'real_free_limit': 0.0, 'total_cards': 0, 'real_limit': 0.0}


Wallet has following properties:
*  max_limit: maximum limit (summing all cards limits)
*  total_used: total used credit in wallet
*  real_limit: the real limit imposed by the user
*  free_limit: limit that can be used, considered maximum limit of card
*  real_free_limit: free limit considering the real limit
*  total_cards: Total number of cards

## Add card to wallet

To increase wallet limit we will include some cards in it:


```python
card0_arguments = dict(number='378282246310005',
                      due_day=13,
                      expiration_date='06/12/2068',
                      cvv='987',
                      max_limit=500.0)
r = req.post(api('wallet/cards'), data=card0_arguments, headers=headers)
card0 = r.json()
print(card0)
```

    {'due_date': 'Wed, 13 Sep 2017 00:00:00 GMT', 'free_limit': 500.0, 'max_limit': 500.0, 'active': True, 'expiration_date': 'Tue, 12 Jun 2068 00:00:00 GMT', 'uid': '280e3abd60a748ed8f0d75d060397ad9'}


based on already seen, card attributes are very clear. Sensible data like number and cvv are not got back.

Once we add a card, wallet limits are different:


```python
r = req.get(api('wallet'), headers=headers)
wallet = r.json()
print(wallet)
```

    {'total_used': 0.0, 'free_limit': 500.0, 'max_limit': 500.0, 'real_free_limit': 500.0, 'total_cards': 1, 'real_limit': 500.0}


### Adding more cards

As expected, wallet limits was increased by cards limit. Adding another card will produce an expected result:


```python
card1_arguments = dict(number='5078601870000127985',
                      due_day=13,
                      expiration_date='11/16/2028',
                      cvv='335',
                      max_limit=550.0)
r = req.post(api('wallet/cards'), data=card1_arguments, headers=headers)
card1 = r.json()
print(card1)
```

    {'due_date': 'Wed, 13 Sep 2017 00:00:00 GMT', 'free_limit': 550.0, 'max_limit': 550.0, 'active': True, 'expiration_date': 'Thu, 16 Nov 2028 00:00:00 GMT', 'uid': '370646ebe5424eac801e2d32d4557bfe'}



```python
card2_arguments = dict(number='30569309025904',
                      due_day=13,
                      expiration_date='01/20/2040',
                      cvv='654',
                      max_limit=2000.0)
r = req.post(api('wallet/cards'), data=card2_arguments, headers=headers)
card2 = r.json()
print(card2)
```

    {'due_date': 'Wed, 13 Sep 2017 00:00:00 GMT', 'free_limit': 2000.0, 'max_limit': 2000.0, 'active': True, 'expiration_date': 'Fri, 20 Jan 2040 00:00:00 GMT', 'uid': 'b0fb8906d271465889904e7bbebfa701'}



```python
card3_arguments = dict(number='6011111111111117',
                      due_day=20,
                      expiration_date='01/20/2060',
                      cvv='365',
                      max_limit=1000.0)
r = req.post(api('wallet/cards'), data=card3_arguments, headers=headers)
card3 = r.json()
print(card3)
```

    {'due_date': 'Wed, 20 Sep 2017 00:00:00 GMT', 'free_limit': 1000.0, 'max_limit': 1000.0, 'active': True, 'expiration_date': 'Tue, 20 Jan 2060 00:00:00 GMT', 'uid': 'cac2172430424323b66d526622417e0f'}



```python
card4_arguments = dict(number='6062825624254001',
                      due_day=3,
                      expiration_date='01/05/2080',
                      cvv='563',
                      max_limit=1000.0)
r = req.post(api('wallet/cards'), data=card4_arguments, headers=headers)
card4 = r.json()
print(card4)
```

    {'due_date': 'Sun, 03 Sep 2017 00:00:00 GMT', 'free_limit': 1000.0, 'max_limit': 1000.0, 'active': True, 'expiration_date': 'Fri, 05 Jan 2080 00:00:00 GMT', 'uid': 'f7ae1b43d9144283bf738515bac2c5ab'}



```python
card5_arguments = dict(number='6062825624254001',
                      due_day=25,
                      expiration_date='01/05/2080',
                      cvv='563',
                      max_limit=100.0)
r = req.post(api('wallet/cards'), data=card5_arguments, headers=headers)
card5 = r.json()
print(card5)
```

    {'due_date': 'Mon, 25 Sep 2017 00:00:00 GMT', 'free_limit': 100.0, 'max_limit': 100.0, 'active': True, 'expiration_date': 'Fri, 05 Jan 2080 00:00:00 GMT', 'uid': 'ef4a5093f7c34148aa75e5880c67efc0'}


### New wallet limits

After addind these cards, we could take a look at wallet limits and make more analysis:


```python
r = req.get(api('wallet'), headers=headers)
wallet = r.json()
print(wallet)
```

    {'total_used': 0.0, 'free_limit': 5150.0, 'max_limit': 5150.0, 'real_free_limit': 5150.0, 'total_cards': 6, 'real_limit': 5150.0}


As expected, wallet limit is the sum of all cards.

Now we can change wallet real limit:


```python
r = req.put(api('wallet/real_limit/{}').format(3000.0), headers=headers)
wallet = r.json()
print(wallet)
```

    {'total_used': 0.0, 'free_limit': 5150.0, 'max_limit': 5150.0, 'real_free_limit': 3000.0, 'total_cards': 6, 'real_limit': 3000.0}


Now, *real_limit* and *real_free_limit* are set to 3000. We can make a new get request and confirm value is changed:


```python
r = req.get(api('wallet'), headers=headers)
wallet = r.json()
print(wallet)
```

    {'total_used': 0.0, 'free_limit': 5150.0, 'max_limit': 5150.0, 'real_free_limit': 3000.0, 'total_cards': 6, 'real_limit': 3000.0}


Now, we may add a new card:


```python
card3_arguments = dict(number='6362970000457013',
                      due_day=5,
                      expiration_date='05/3/2028',
                      cvv='449',
                      max_limit=6000.0)
r = req.post(api('wallet/cards'), data=card3_arguments, headers=headers)
card3 = r.json()
print(card3)
```

    {'due_date': 'Tue, 05 Sep 2017 00:00:00 GMT', 'free_limit': 6000.0, 'max_limit': 6000.0, 'active': True, 'expiration_date': 'Wed, 03 May 2028 00:00:00 GMT', 'uid': '1b73852dde024a80b450aa71934785f5'}


After adding these card, we may analyse new wallet limits:


```python
r = req.get(api('wallet'), headers=headers)
wallet = r.json()
print(wallet)
```

    {'total_used': 0.0, 'free_limit': 11150.0, 'max_limit': 11150.0, 'real_free_limit': 3000.0, 'total_cards': 7, 'real_limit': 3000.0}


As expected, *max_limit* and *free_limit* were increased by card limit, but *real_limit* and *real_free_limit* are not changed anymore.

if we try changing *real_limit* to a value greater than *max_limit * we get an error:


```python
r = req.put(api('wallet/real_limit/{}').format(12000.0), headers=headers)
wallet = r.json()
print(wallet)
```

    {'error': 'Real Limit exceeds maximum permited'}


And *real_limit* keeps the same:


```python
r = req.get(api('wallet'), headers=headers)
wallet = r.json()
print(wallet)
```

    {'total_used': 0.0, 'free_limit': 11150.0, 'max_limit': 11150.0, 'real_free_limit': 3000.0, 'total_cards': 7, 'real_limit': 3000.0}


### Deactivating some cards

We add cards, now, removing cards should reduce wallet limit:


```python
r = req.delete(api('wallet/cards/{}').format(card3['uid']), headers=headers)
card3 = r.json()
print(card3)
```

    {'due_date': 'Tue, 05 Sep 2017 00:00:00 GMT', 'free_limit': 6000.0, 'max_limit': 6000.0, 'active': False, 'expiration_date': 'Wed, 03 May 2028 00:00:00 GMT', 'uid': '1b73852dde024a80b450aa71934785f5'}



```python
r = req.get(api('wallet'), headers=headers)
wallet = r.json()
print(wallet)
```

    {'total_used': 0.0, 'free_limit': 5150.0, 'max_limit': 5150.0, 'real_free_limit': 3000.0, 'total_cards': 7, 'real_limit': 3000.0}


*card2* has a limit of 2000:


```python
print(card2['max_limit'])
```

    2000.0


Removing card2 make wallet max_limit bigger than real limit, let's do that:


```python
r = req.delete(api('wallet/cards/{}').format(card2['uid']), headers=headers)
card2 = r.json()
print(card2)
```

    {'due_date': 'Wed, 13 Sep 2017 00:00:00 GMT', 'free_limit': 2000.0, 'max_limit': 2000.0, 'active': False, 'expiration_date': 'Fri, 20 Jan 2040 00:00:00 GMT', 'uid': 'b0fb8906d271465889904e7bbebfa701'}



```python
r = req.get(api('wallet'), headers=headers)
wallet = r.json()
print(wallet)
```

    {'total_used': 0.0, 'free_limit': 3150.0, 'max_limit': 3150.0, 'real_free_limit': 3000.0, 'total_cards': 7, 'real_limit': 3000.0}


Now, wallet's free_limit was reduced, once it cannot be the value it was before.

## Purchasing

Purchasing in a wallet should select best card/cards according to problem defined rules. Let's revisit cards limit again:


```python
r = req.get(api('wallet/cards'), headers=headers)
cards = r.json()
print(cards)
```

    {'cards': [{'due_date': 'Tue, 05 Sep 2017 00:00:00 GMT', 'free_limit': 6000.0, 'max_limit': 6000.0, 'active': False, 'expiration_date': 'Wed, 03 May 2028 00:00:00 GMT', 'uid': '1b73852dde024a80b450aa71934785f5'}, {'due_date': 'Mon, 25 Sep 2017 00:00:00 GMT', 'free_limit': 100.0, 'max_limit': 100.0, 'active': True, 'expiration_date': 'Fri, 05 Jan 2080 00:00:00 GMT', 'uid': 'ef4a5093f7c34148aa75e5880c67efc0'}, {'due_date': 'Sun, 03 Sep 2017 00:00:00 GMT', 'free_limit': 1000.0, 'max_limit': 1000.0, 'active': True, 'expiration_date': 'Fri, 05 Jan 2080 00:00:00 GMT', 'uid': 'f7ae1b43d9144283bf738515bac2c5ab'}, {'due_date': 'Wed, 20 Sep 2017 00:00:00 GMT', 'free_limit': 1000.0, 'max_limit': 1000.0, 'active': True, 'expiration_date': 'Tue, 20 Jan 2060 00:00:00 GMT', 'uid': 'cac2172430424323b66d526622417e0f'}, {'due_date': 'Wed, 13 Sep 2017 00:00:00 GMT', 'free_limit': 2000.0, 'max_limit': 2000.0, 'active': False, 'expiration_date': 'Fri, 20 Jan 2040 00:00:00 GMT', 'uid': 'b0fb8906d271465889904e7bbebfa701'}, {'due_date': 'Wed, 13 Sep 2017 00:00:00 GMT', 'free_limit': 550.0, 'max_limit': 550.0, 'active': True, 'expiration_date': 'Thu, 16 Nov 2028 00:00:00 GMT', 'uid': '370646ebe5424eac801e2d32d4557bfe'}, {'due_date': 'Wed, 13 Sep 2017 00:00:00 GMT', 'free_limit': 500.0, 'max_limit': 500.0, 'active': True, 'expiration_date': 'Tue, 12 Jun 2068 00:00:00 GMT', 'uid': '280e3abd60a748ed8f0d75d060397ad9'}], 'wid': 'ac263724cef1492f947fe819df6166f6'}


Here we have wallet wid and card list. We have to filter for active cards, because only then will be used in purchases. But there is a better solution, using cards already sorted and prepared for purhase:


```python
r = req.get(api('wallet/cards/sorted'), headers=headers)
cards = r.json()
print(cards)
```

    {'cards': [{'due_date': 'Mon, 25 Sep 2017 00:00:00 GMT', 'free_limit': 100.0, 'max_limit': 100.0, 'active': True, 'expiration_date': 'Fri, 05 Jan 2080 00:00:00 GMT', 'uid': 'ef4a5093f7c34148aa75e5880c67efc0'}, {'due_date': 'Wed, 20 Sep 2017 00:00:00 GMT', 'free_limit': 1000.0, 'max_limit': 1000.0, 'active': True, 'expiration_date': 'Tue, 20 Jan 2060 00:00:00 GMT', 'uid': 'cac2172430424323b66d526622417e0f'}, {'due_date': 'Wed, 13 Sep 2017 00:00:00 GMT', 'free_limit': 500.0, 'max_limit': 500.0, 'active': True, 'expiration_date': 'Tue, 12 Jun 2068 00:00:00 GMT', 'uid': '280e3abd60a748ed8f0d75d060397ad9'}, {'due_date': 'Wed, 13 Sep 2017 00:00:00 GMT', 'free_limit': 550.0, 'max_limit': 550.0, 'active': True, 'expiration_date': 'Thu, 16 Nov 2028 00:00:00 GMT', 'uid': '370646ebe5424eac801e2d32d4557bfe'}, {'due_date': 'Sun, 03 Sep 2017 00:00:00 GMT', 'free_limit': 1000.0, 'max_limit': 1000.0, 'active': True, 'expiration_date': 'Fri, 05 Jan 2080 00:00:00 GMT', 'uid': 'f7ae1b43d9144283bf738515bac2c5ab'}], 'wid': 'ac263724cef1492f947fe819df6166f6'}


Next I will create a simple helper function to get cards and print their uid, max_limit, free_limit and due_date with some wallet summary:


```python
def get_cards_status():
    r = req.get(api('wallet'), headers=headers)
    wallet = r.json()
    
    r = req.get(api('wallet/cards/sorted'), headers=headers)
    cards = r.json()
    
    print('*'*50)
    print('Wallet, ', datetime.today())
    print('='*50)
    print("real_limit: ", wallet['real_limit'])
    print("free_limit: ", wallet['free_limit'])
    print("real_free_limit: ", wallet['real_free_limit'])
    print("total_cards: ", wallet['total_cards'])
    print("total_used: ", wallet['total_used'])
    print("max_limit: ", wallet['max_limit'])
    
    print('='*50)
    print("Cards")
    print('='*50)
    for card in cards['cards']:
        print(card['uid'])
        print('max_limit: ', card['max_limit'])
        print('free_limit: ', card['free_limit'])
        print('due_date: ', card['due_date'])
        print('-'*50)
```


```python
get_cards_status()
```

    **************************************************
    Wallet,  2017-08-29 19:58:02.123055
    ==================================================
    real_limit:  3000.0
    free_limit:  3150.0
    real_free_limit:  3000.0
    total_cards:  7
    total_used:  0.0
    max_limit:  3150.0
    ==================================================
    Cards
    ==================================================
    ef4a5093f7c34148aa75e5880c67efc0
    max_limit:  100.0
    free_limit:  100.0
    due_date:  Mon, 25 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    cac2172430424323b66d526622417e0f
    max_limit:  1000.0
    free_limit:  1000.0
    due_date:  Wed, 20 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    280e3abd60a748ed8f0d75d060397ad9
    max_limit:  500.0
    free_limit:  500.0
    due_date:  Wed, 13 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    370646ebe5424eac801e2d32d4557bfe
    max_limit:  550.0
    free_limit:  550.0
    due_date:  Wed, 13 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    f7ae1b43d9144283bf738515bac2c5ab
    max_limit:  1000.0
    free_limit:  1000.0
    due_date:  Sun, 03 Sep 2017 00:00:00 GMT
    --------------------------------------------------


Purchasing rules depends on how far card's due date is from today, it is, the card selection on purchase will vary day by day.

In the momentt of writting, sorting is:

```
==================================================
Cards
==================================================
ef4a5093f7c34148aa75e5880c67efc0
max_limit:  100.0
free_limit:  100.0
due_date:  Mon, 25 Sep 2017 00:00:00 GMT
--------------------------------------------------
cac2172430424323b66d526622417e0f
max_limit:  1000.0
free_limit:  1000.0
due_date:  Wed, 20 Sep 2017 00:00:00 GMT
--------------------------------------------------
280e3abd60a748ed8f0d75d060397ad9
max_limit:  500.0
free_limit:  500.0
due_date:  Wed, 13 Sep 2017 00:00:00 GMT
--------------------------------------------------
370646ebe5424eac801e2d32d4557bfe
max_limit:  550.0
free_limit:  550.0
due_date:  Wed, 13 Sep 2017 00:00:00 GMT
--------------------------------------------------
f7ae1b43d9144283bf738515bac2c5ab
max_limit:  1000.0
free_limit:  1000.0
due_date:  Sun, 03 Sep 2017 00:00:00 GMT
--------------------------------------------------
```

THis way, first card is due_day 25 max_limit 100.0, if I do a Purchase of 50, it would use this card:


```python
r = req.post(api('wallet/purchase'), data=dict(value=50), headers=headers)
purchase = r.json()
print(purchase)
```

    {'total': 50.0, 'relations': {'date_time': 'Tue, 29 Aug 2017 23:02:49 GMT', 'value': 50.0, 'cid': 'ef4a5093f7c34148aa75e5880c67efc0'}, 'wid': 'ac263724cef1492f947fe819df6166f6'}


This is a purchase object. The **cid** parameter is the *c*ard u*id*, following same convention used for *w*allet u*id*. We can see by cid that the card used for purchase is the one expected.


```python
get_cards_status()
```

    **************************************************
    Wallet,  2017-08-29 20:04:59.136030
    ==================================================
    real_limit:  3000.0
    free_limit:  3100.0
    real_free_limit:  2950.0
    total_cards:  7
    total_used:  50.0
    max_limit:  3150.0
    ==================================================
    Cards
    ==================================================
    ef4a5093f7c34148aa75e5880c67efc0
    max_limit:  100.0
    free_limit:  50.0
    due_date:  Mon, 25 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    cac2172430424323b66d526622417e0f
    max_limit:  1000.0
    free_limit:  1000.0
    due_date:  Wed, 20 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    280e3abd60a748ed8f0d75d060397ad9
    max_limit:  500.0
    free_limit:  500.0
    due_date:  Wed, 13 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    370646ebe5424eac801e2d32d4557bfe
    max_limit:  550.0
    free_limit:  550.0
    due_date:  Wed, 13 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    f7ae1b43d9144283bf738515bac2c5ab
    max_limit:  1000.0
    free_limit:  1000.0
    due_date:  Sun, 03 Sep 2017 00:00:00 GMT
    --------------------------------------------------


As expected, wallet and selected card free limits are changed according to value purchased.
Now, a new purchase which cannot be done in first card will be done in second one:


```python
r = req.post(api('wallet/purchase'), data=dict(value=500), headers=headers)
purchase = r.json()
print(purchase)
```

    {'total': 500.0, 'relations': {'date_time': 'Tue, 29 Aug 2017 23:07:29 GMT', 'value': 500.0, 'cid': 'cac2172430424323b66d526622417e0f'}, 'wid': 'ac263724cef1492f947fe819df6166f6'}



```python
get_cards_status()
```

    **************************************************
    Wallet,  2017-08-29 20:07:51.210303
    ==================================================
    real_limit:  3000.0
    free_limit:  2600.0
    real_free_limit:  2450.0
    total_cards:  7
    total_used:  550.0
    max_limit:  3150.0
    ==================================================
    Cards
    ==================================================
    ef4a5093f7c34148aa75e5880c67efc0
    max_limit:  100.0
    free_limit:  50.0
    due_date:  Mon, 25 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    cac2172430424323b66d526622417e0f
    max_limit:  1000.0
    free_limit:  500.0
    due_date:  Wed, 20 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    280e3abd60a748ed8f0d75d060397ad9
    max_limit:  500.0
    free_limit:  500.0
    due_date:  Wed, 13 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    370646ebe5424eac801e2d32d4557bfe
    max_limit:  550.0
    free_limit:  550.0
    due_date:  Wed, 13 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    f7ae1b43d9144283bf738515bac2c5ab
    max_limit:  1000.0
    free_limit:  1000.0
    due_date:  Sun, 03 Sep 2017 00:00:00 GMT
    --------------------------------------------------


Now, a purchase of 1100 can't be done in only one card, it will be distributed in may cards respecting sorting order:


```python
r = req.post(api('wallet/purchase'), data=dict(value=1100), headers=headers)
purchase = r.json()
print(purchase)
```

    {'total': 1100.0, 'relations': {'date_time': 'Tue, 29 Aug 2017 23:10:49 GMT', 'value': 50.0, 'cid': 'ef4a5093f7c34148aa75e5880c67efc0'}, 'wid': 'ac263724cef1492f947fe819df6166f6'}



```python
get_cards_status()
```

    **************************************************
    Wallet,  2017-08-29 20:10:56.053262
    ==================================================
    real_limit:  3000.0
    free_limit:  1500.0
    real_free_limit:  1350.0
    total_cards:  7
    total_used:  1650.0
    max_limit:  3150.0
    ==================================================
    Cards
    ==================================================
    ef4a5093f7c34148aa75e5880c67efc0
    max_limit:  100.0
    free_limit:  0.0
    due_date:  Mon, 25 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    cac2172430424323b66d526622417e0f
    max_limit:  1000.0
    free_limit:  0.0
    due_date:  Wed, 20 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    280e3abd60a748ed8f0d75d060397ad9
    max_limit:  500.0
    free_limit:  0.0
    due_date:  Wed, 13 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    370646ebe5424eac801e2d32d4557bfe
    max_limit:  550.0
    free_limit:  500.0
    due_date:  Wed, 13 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    f7ae1b43d9144283bf738515bac2c5ab
    max_limit:  1000.0
    free_limit:  1000.0
    due_date:  Sun, 03 Sep 2017 00:00:00 GMT
    --------------------------------------------------


A purchase of 12000 will not be processed because exceeds wallet limit. It should return an error:


```python
r = req.post(api('wallet/purchase'), data=dict(value=12000), headers=headers)
purchase = r.json()
print(purchase)
```

    {'error': 'Real limit exceed'}


And limits are kept the same:


```python
get_cards_status()
```

    **************************************************
    Wallet,  2017-08-29 20:15:03.959828
    ==================================================
    real_limit:  3000.0
    free_limit:  1500.0
    real_free_limit:  1350.0
    total_cards:  7
    total_used:  1650.0
    max_limit:  3150.0
    ==================================================
    Cards
    ==================================================
    ef4a5093f7c34148aa75e5880c67efc0
    max_limit:  100.0
    free_limit:  0.0
    due_date:  Mon, 25 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    cac2172430424323b66d526622417e0f
    max_limit:  1000.0
    free_limit:  0.0
    due_date:  Wed, 20 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    280e3abd60a748ed8f0d75d060397ad9
    max_limit:  500.0
    free_limit:  0.0
    due_date:  Wed, 13 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    370646ebe5424eac801e2d32d4557bfe
    max_limit:  550.0
    free_limit:  500.0
    due_date:  Wed, 13 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    f7ae1b43d9144283bf738515bac2c5ab
    max_limit:  1000.0
    free_limit:  1000.0
    due_date:  Sun, 03 Sep 2017 00:00:00 GMT
    --------------------------------------------------


## Paying

We purchase with these cards, a good next step is releasing credit with payment. The rule for payment is: the user should select which card to pay, so, payment is not made for wallet, but for card, and don't folow the purchase rules:


```python
r = req.post(api('wallet/cards/ef4a5093f7c34148aa75e5880c67efc0/pay'), data=dict(value=90.0), headers=headers)
purchase = r.json()
print(purchase)
```

    {'date_time': 'Tue, 29 Aug 2017 23:20:07 GMT', 'value': 90.0, 'cid': 'ef4a5093f7c34148aa75e5880c67efc0', 'wid': 'ac263724cef1492f947fe819df6166f6'}


Now, first card has some credit released:


```python
get_cards_status()
```

    **************************************************
    Wallet,  2017-08-29 20:20:31.058136
    ==================================================
    real_limit:  3000.0
    free_limit:  1590.0
    real_free_limit:  1440.0
    total_cards:  7
    total_used:  1560.0
    max_limit:  3150.0
    ==================================================
    Cards
    ==================================================
    ef4a5093f7c34148aa75e5880c67efc0
    max_limit:  100.0
    free_limit:  90.0
    due_date:  Mon, 25 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    cac2172430424323b66d526622417e0f
    max_limit:  1000.0
    free_limit:  0.0
    due_date:  Wed, 20 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    280e3abd60a748ed8f0d75d060397ad9
    max_limit:  500.0
    free_limit:  0.0
    due_date:  Wed, 13 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    370646ebe5424eac801e2d32d4557bfe
    max_limit:  550.0
    free_limit:  500.0
    due_date:  Wed, 13 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    f7ae1b43d9144283bf738515bac2c5ab
    max_limit:  1000.0
    free_limit:  1000.0
    due_date:  Sun, 03 Sep 2017 00:00:00 GMT
    --------------------------------------------------



```python
r = req.post(api('wallet/cards/cac2172430424323b66d526622417e0f/pay'), data=dict(value=800.0), headers=headers)
purchase = r.json()
print(purchase)
```

    {'date_time': 'Tue, 29 Aug 2017 23:21:26 GMT', 'value': 800.0, 'cid': 'cac2172430424323b66d526622417e0f', 'wid': 'ac263724cef1492f947fe819df6166f6'}



```python
get_cards_status()
```

    **************************************************
    Wallet,  2017-08-29 20:21:46.370285
    ==================================================
    real_limit:  3000.0
    free_limit:  2390.0
    real_free_limit:  2240.0
    total_cards:  7
    total_used:  760.0
    max_limit:  3150.0
    ==================================================
    Cards
    ==================================================
    ef4a5093f7c34148aa75e5880c67efc0
    max_limit:  100.0
    free_limit:  90.0
    due_date:  Mon, 25 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    cac2172430424323b66d526622417e0f
    max_limit:  1000.0
    free_limit:  800.0
    due_date:  Wed, 20 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    280e3abd60a748ed8f0d75d060397ad9
    max_limit:  500.0
    free_limit:  0.0
    due_date:  Wed, 13 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    370646ebe5424eac801e2d32d4557bfe
    max_limit:  550.0
    free_limit:  500.0
    due_date:  Wed, 13 Sep 2017 00:00:00 GMT
    --------------------------------------------------
    f7ae1b43d9144283bf738515bac2c5ab
    max_limit:  1000.0
    free_limit:  1000.0
    due_date:  Sun, 03 Sep 2017 00:00:00 GMT
    --------------------------------------------------


If trying to pay more than a card can receive we get an error:


```python
r = req.post(api('wallet/cards/280e3abd60a748ed8f0d75d060397ad9/pay'), data=dict(value=800.0), headers=headers)
purchase = r.json()
print(purchase)
```

    {'error': 'This payment exceeds maximum card limit'}



```python

```
