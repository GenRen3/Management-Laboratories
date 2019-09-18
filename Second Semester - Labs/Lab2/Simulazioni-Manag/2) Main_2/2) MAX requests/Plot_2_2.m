clear all; close all; clc;
format long


X = [5, 7, 9]

Y_1_1 = [0.0245204360631636, 0.026306636973772033, 0.024882496994065324, 0.026831999959154033, 0.025584914652799755];
var_1_1 = std(Y_1_1);
Y_1_1 = mean(Y_1_1);

Y_1_2 = [0.02509588309415983, 0.027001956200384182, 0.027165285039744046, 0.026614103860130488, 0.02583615076335341];
var_1_2 = std(Y_1_2);
Y_1_2 = mean(Y_1_2);

Y_1_3 = [0.026035659205963072, 0.027252609385768133, 0.025570597068093604, 0.024578004521058006, 0.027768713936701734];
var_1_3 = std(Y_1_3);
Y_1_3 = mean(Y_1_3);
 
Y1 = [Y_1_1, Y_1_2, Y_1_3]
err1 = [var_1_1, var_1_2, var_1_3]







Y_2_1 = [0.30700698633108026, 0.3267067766413651, 0.3105838776614179, 0.3325284058427605, 0.31855151355484085];
var_2_1 = std(Y_2_1);
Y_2_1 = mean(Y_2_1);

Y_2_2 = [0.31327795881408405, 0.33447289683740467, 0.33577970241148297, 0.3298943161789702, 0.3212947938446492];
var_2_2 = std(Y_2_2);
Y_2_2 = mean(Y_2_2);

Y_2_3 = [0.32358656722217174, 0.33692385199989744, 0.3188369346903639, 0.3276980746832646, 0.34274664951417716];
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



xlabel('Max Request = 5, 7, 9');

ylabel('Mean values');

legend('Location','northeast')
legend('Average RTT','Average service time')