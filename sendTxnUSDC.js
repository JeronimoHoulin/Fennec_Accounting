import { ethers } from "ethers";
import { USDC_Polygo_Adrs } from "../Constants/USDC";
import { ERC20_abi } from "../Constants/ERC20_abi";

export async function sendTxnUSDC(fromadrs, amount_usdc){

    const provider = new ethers.providers.Web3Provider(window.ethereum, "any");
    const signer = provider.getSigner();

    const usdc = new ethers.Contract(USDC_Polygo_Adrs, ERC20_abi, signer);
    //let decimals = 6;

    let to = "0x0c256b7b7d7c94b7f561b33f507d45b5924f1bb1"; //OKX

    let value;
    let toAdrs;
    
    try{
        toAdrs = ethers.utils.getAddress(to);
    }catch{
        console.log("Invalid address: ", fromadrs);
        process.exit(1);
    }

    try{
        value = amount_usdc;
        //console.log("We will send: ", value)
        if(value < 0){
            throw new Error();
        }
    }catch{
        console.log("Invalid amount: ", value);
        process.exit(1);
    }

    const balance = await usdc.balanceOf(fromadrs)
    const tokenUnits = await usdc.decimals();
    const balanceInUsdc = ethers.utils.formatUnits(balance, tokenUnits);

    if(Number(balanceInUsdc) < Number(value)) {
        console.error(
            `Insuficient balance to send ${value} (you have ${balanceInUsdc})`
        );
    }

    //console.log("value to send : ", ethers.utils.parseUnits(String(value), 6))

    const tx = await usdc.transfer(toAdrs, ethers.utils.parseUnits(String(value), 6))
    console.log("Transaction hash: ", tx.hash);
    /* THIS TAKES A WHILE LONGER.. not sure if needed (NOW THAT WE VALIDATE WITH OKX AND NOT POLYGONSCAN)
    const recipt = await tx.wait();
    console.log("Transaction confirmed in block:", recipt.blockNumber);
    console.log("Type of txn hash: ",typeof(tx.hash));
    */
    //tx.hash  or String(tx.hash)

    return tx.hash;

}