clear all; close all; clc;
format long


X = [125*10^3, 10^6, 10^9]

Y_1_1 = [0.004677614908919705, 0.004674625960997122, 0.004683277874717915, 0.004681529103665678, 0.004673811199073114];
var_1_1 = std(Y_1_1);
Y_1_1 = mean(Y_1_1);

Y_1_2 = [0.004688552363498583, 0.0046895752395184655, 0.004678634999597824, 0.004672783911033111, 0.004683152730952887];
var_1_2 = std(Y_1_2);
Y_1_2 = mean(Y_1_2);

Y_1_3 = [0.004682295307456175, 0.004685890699798105, 0.004684386830061482, 0.0046850113284270705, 0.004679993511065525];
var_1_3 = std(Y_1_3);
Y_1_3 = mean(Y_1_3);
 
Y1 = [Y_1_1, Y_1_2, Y_1_3]
err1 = [var_1_1, var_1_2, var_1_3]


Y_2_1 = [0.15134128610284792, 0.15143079899895648, 0.1515902452212504, 0.15155419324449898, 0.15136964395853864];
var_2_1 = std(Y_2_1);
Y_2_1 = mean(Y_2_1);

Y_2_2 = [0.08846655400622466, 0.08848943984460625, 0.08840465644725415, 0.0882871009243514, 0.08838248666863698];
var_2_2 = std(Y_2_2);
Y_2_2 = mean(Y_2_2);

Y_2_3 = [0.08175629485437502, 0.08176586649040836, 0.08183613814755859, 0.08180858478178532, 0.08176139746301717];
var_2_3 = std(Y_2_3);
Y_2_3 = mean(Y_2_3);

Y2 = [Y_2_1, Y_2_2, Y_2_3]
err2 = [var_2_1, var_2_2, var_2_3]



figure(1);

title('Average RTT and Average Service Time over 24 hours');
hold on

%plot([1000, 1000000, 1000000000], [Y_1_1, Y_1_2, Y_1_3])
%plot([1000, 1000000, 1000000000], [Y_2_1, Y_2_2, Y_2_3])

%errorbar(X,Y1,err1, '-s','MarkerSize',10,'MarkerEdgeColor','red','MarkerFaceColor','blue', 'Linewidth',2)
errorbar(X,Y2,err2, '-s','MarkerSize',10,'MarkerEdgeColor','red','MarkerFaceColor','blue', 'Linewidth',2)
set(gca,'XScale','log');
set(gca,'YScale','log');

grid on



xlabel('Link capacities = 125*10^3 (kbps), 10^6 (Mbps), 10^9 (Gbps)');

ylabel('Mean values');

legend('Location','northeast')
legend('Average RTT','Average service time')
