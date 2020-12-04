If you found this repo useful, consider hitting the 'sponsor' button near the top :)



# Redirect.comBuyingAndZeroPark.comSelling
A script that maximizes inputs and outputs to optimize profits while buying traffic on Redirect.com and selling on ZeroPark.com

This script expects a file results.txt with campaign names then a comma then campaign IDs from Redirect.com.

This script expects your target URL for ZeroPark to have the Target name (ie. the part of the URL preceding the ?) to match exactly the Campaign Name as specified on Redirect.com.

Don't use the provided results.txt file - replace it with your own campaigns.

The 'rate' variable reflects the expected ROI from the script. At 2.05, you can expect this script to usually return 205% ROI. The lower the value, the more traffic and the higher the cost.

The script will first try to accurately determine the CPM of a given campaign, by dividing the revenues shown on ZeroPark with the total traffic sent from Redirect.com over the last 3 calendar days. If it can't make this calculation, it will 'guess' the CPM by dividing the CPM reported on ZeroPark by a constant.

Next, it will set an optimised bid based on the 'rate' variable.

For those low-CPM campaigns (think Geos like China, India) it will then re-adjust the bid to be more than $0.20 (the bare minimum to receive traffic) based on some factors - but will always remain profitable.

Thanks for having a look!

-Jarett
