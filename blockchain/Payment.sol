pragma solidity ^0.5.0;

contract Payment {
    //structs of buyers,sellers and item
    struct Buyer {
        uint weight;
        uint balance;
        bool bought;
        uint8 item;
    }
    struct Seller {
        uint weight;
        uint balance;
        bool sold;
        uint8 item;
    }
    //number of item to buy 
    struct Item {
        uint itemCount;
        uint8 itemPrice;
        bool forSale;
    }
    
    //controls who can register and buy/sell
    address chairperson;
    //address payable owner;
    mapping(address => Buyer) buyers; 
    mapping(address => Seller) sellers;
    //mapping (address => uint) public balances;
    Item[] public items; // stores items for sale 
   
    //states of buying an item 
    enum Phase {Init,Regs, Buy, Sold, Done}  
    Phase public state = Phase.Done; 
    
    //modifiers
    modifier validPhase(Phase reqPhase) 
    { 
        require(state == reqPhase); 
        _; 
    }
    modifier onlyChair() 
    {
        require(msg.sender == chairperson);
        _;
    } 

    uint public startTime;//keep track of time
    
    constructor(uint8 numItems, uint8 price) public  {
        chairperson = msg.sender;
        buyers[chairperson].weight = 2; // weight 2 for testing purposes
        sellers[chairperson].weight = 2; // make account 1 as the only seller for now
        items.length = numItems;
        //for now initialize items with the same price and 
        //add them for sale
        for(uint8 i = 0; i < items.length;i++){
            items[i].itemPrice = price;
            items[i].forSale = true;
        }    
        state = Phase.Regs;
        startTime = now; //start time now at constructor call
    }

    
    //Register - Add new user, give them 500 balance.
    function register(address buyer) public validPhase(Phase.Regs) onlyChair {
        buyers[buyer].weight = 1;
        buyers[buyer].bought = false;
        buyers[buyer].balance = 500;
        if (now > (startTime+ 30 seconds)) {state = Phase.Buy; }     
    }
    //Unregister - Remove user, take their money. 
    function unregister(address buyer) public validPhase(Phase.Done) onlyChair {
     //   require ( voters[voter].voted);
        buyers[buyer].weight = 0;
        buyers[buyer].bought = false;
        buyers[buyer].balance = 0;
        if (now > (startTime+ 30 seconds)) {state = Phase.Init; }     
    }

    //Buy - This will record the transaction between 2 users.
    function buy(address buyer,uint8 itemId) public validPhase(Phase.Buy){
        //Buyer memory sender = buyers[buyer];
        //check to see if buyer already bought or item is not available
        if (buyers[buyer].bought || itemId >= items.length 
           || !items[itemId].forSale  || buyers[buyer].weight == 0) return; 
        buyers[buyer].bought = true;//mark item as bought
        buyers[buyer].item = itemId;   
        items[itemId].itemCount += buyers[buyer].weight; // increase items added to cart
        items[itemId].forSale = false; //mark item as sold
        if (now > (startTime+ 60 seconds)) {state = Phase.Sold; }   
    }
    //Settle/Pay - Transfers money from buyer to seller. //chairperson is the only seller for now
    function pay(address receiver,uint balance) public validPhase(Phase.Sold){
        //Seller memory receiver = sellers[chairperson];
        
        Buyer memory sender = buyers[msg.sender];
        //check to see if buyer didn't buy or they are unregistered
        //and seller is selling 
        if ( !sender.bought || sellers[receiver].sold ||sender.weight == 0) return; 
        sellers[receiver].balance += balance;
        sender.balance -= balance;
        if (now > (startTime+ 75 seconds)) {state = Phase.Done; }  
    }
    //Deposit - Adds funds to users balance.
    function deposit(address buyer,uint money) public  {
        buyers[buyer].balance += money;  
    }
    
    //Withdraw - Take funds from users balance.
    function withdraw(address buyer,uint money) public  {
        buyers[buyer].balance -= money;  
    }
    
    //getters
    function getBalance(address buyer) public view returns(uint,uint){
        Buyer memory sender = buyers[buyer];
        Seller memory receiver = sellers[chairperson];
        return (sender.balance,receiver.balance); 
        

    }
    function getState() public view returns (Phase){
        return state;
    }
    function getbuyer() public view returns (Buyer memory,Seller memory){
        Buyer memory sender = buyers[msg.sender];
        Seller memory receiver = sellers[chairperson];
        return (sender,receiver);
    }
    
}
