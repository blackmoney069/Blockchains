// Bainscoin ICO

//version of the compiler
pragma solidity ^0.4.11;

contract Bainscoin_ico{
    
    // total supply of bainscoins
    uint public max_bainscoin = 1000000;
    
    // exchange rate against USD
    uint public usd_to_bainscoin = 1000;
    
    // circulating supply
    uint public circulating_supply = 0;
    
    // mapping from the investors address to its equity in bainscoins and USD 
    mapping(address => uint) equity_bainscoin;          // the mapping will take address as the input and will return a uint of name equity_bainscoin
    mapping(address => uint) equity_usd;                 // the mapping will take address as the input and will return a uint of name equity_usd
    
    //check if investor can buy a Bainscoin during the ICO
    modifier can_buy_bainscoin(uint usd_invested){
        require(usd_invested*usd_to_bainscoin+circulating_supply <= max_bainscoin);
        _; 
    }
    
    // function to get the quity of the investor in Bainscoin
    function equity_in_bainscoin(address investor) external constant returns(uint){
        return equity_bainscoin[investor];
    }
    
    // function to get the quity of the investor in USD
    function equity_in_usd(address investor) external constant returns(uint){
        return equity_usd[investor];
    }
    
    // buy bainscoins 
    function buy_bainscoin(address investor, uint usd_invested) external
    can_buy_bainscoin(usd_invested){
        uint bainscoin_bought = usd_invested*usd_to_bainscoin;
        equity_bainscoin[investor] += bainscoin_bought;
        
        circulating_supply += bainscoin_bought;
        
        equity_usd[investor] = equity_bainscoin[investor]/usd_to_bainscoin;
    }
    
    // selling bainscoins
    function sell_bainscoin(address investor, uint bainscoins_sold) external{
        equity_bainscoin[investor] -= bainscoins_sold;
        circulating_supply -= bainscoins_sold;
        equity_usd[investor] = equity_bainscoin[investor]/usd_to_bainscoin;
    }

}

