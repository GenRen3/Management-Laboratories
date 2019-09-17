clear all; close all; clc;
format long


X = [125*10^3, 10^6, 10^9]

Y_1_1 = [0.019177585751393427, 0.018734963020678997, 0.017945080164704745, 0.018885948644129923, 0.019866767183333047];
var_1_1 = std(Y_1_1);
Y_1_1 = mean(Y_1_1);

Y_1_2 = [0.02822787751685921, 0.024335189736260608, 0.02589973604094722, 0.024930634870464718, 0.02625180639172046];
var_1_2 = std(Y_1_2);
Y_1_2 = mean(Y_1_2);

Y_1_3 = [0. 02648818974365844, 0.027562379721120057, 0.025052896228482467, 0.0268978761230759, 0.0268978761230759];
var_1_3 = std(Y_1_3);
Y_1_3 = mean(Y_1_3);
 
Y1 = [Y_1_1, Y_1_2, Y_1_3]
err1 = [var_1_1, var_1_2, var_1_3]







Y_2_1 = [0.34709512054169767, 0.3412787845928053, 0.3294788596715361, 0.34262724360002583, 0.35131623039330107];
var_2_1 = std(Y_2_1);
Y_2_1 = mean(Y_2_1);

Y_2_2 = [0.3477869585991692, 0.3049497936972061, 0.3221465365336084, 0.31170751989291523, 0.326218602915366];
var_2_2 = std(Y_2_2);
Y_2_2 = mean(Y_2_2);

Y_2_3 = [0.3218892470283265, 0.3335253562528093, 0.3059344467721246, 0.3263321189367103, 0.3263321189367103];
var_2_3 = std(Y_2_3);
Y_2_3 = mean(Y_2_3);

Y2 = [Y_2_1, Y_2_2, Y_2_3]
err2 = [var_2_1, var_2_2, var_2_3]



figure(1);

title('Average RTT and Average Service Time over 24 hours');
hold on



%errorbar(X,Y1,err1, '-s','MarkerSize',10,'MarkerEdgeColor','red','MarkerFaceColor','blue', 'Linewidth',2)
errorbar(X,Y2,err2, '-s','MarkerSize',10,'MarkerEdgeColor','red','MarkerFaceColor','blue', 'Linewidth',2)
set(gca,'XScale','log');
set(gca,'YScale','log');

grid on



xlabel('Link capacities = 125*10^3 (kbps), 10^6 (Mbps), 10^9 (Gbps)');

ylabel('Mean values');

legend('Location','northeast')
legend('Average RTT','Average service time')