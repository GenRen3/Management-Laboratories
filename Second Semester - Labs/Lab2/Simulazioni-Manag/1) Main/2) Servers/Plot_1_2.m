clear all; close all; clc;
format long


X = [3, 16, 52]

Y_1_1 = [0.010507101277989865, 0.010487213989764432, 0.010507622193490563, 0.01050551365020543, 0.010502991713016887];
var_1_1 = var(Y_1_1);
Y_1_1 = mean(Y_1_1);

Y_1_2 = [0.004683752819934672, 0.004679884892180213, 0.00468065976988665, 0.00469065972582165, 0.00467865269847634];
var_1_2 = var(Y_1_2);
Y_1_2 = mean(Y_1_2);

Y_1_3 = [0.00378816179640811, 0.003788704853901274, 0.003788667611981513, 0.003795905267672189, 0.0037880069753763717];
var_1_3 = var(Y_1_3);
Y_1_3 = mean(Y_1_3);
 
Y1 = [Y_1_1, Y_1_2, Y_1_3];
err1 = [var_1_1, var_1_2, var_1_3];









Y_2_1 = [0.15271029552389292, 0.15227958994151525, 0.15265107264201383, 0.15246867121939292, 0.15252291957247027];
var_2_1 = var(Y_2_1);
Y_2_1 = mean(Y_2_1);

Y_2_2 = [0.08848502154687682, 0.08835309684723344, 0.08833027032140417, 0.08832952584713634, 0.08832268435725344];
var_2_2 = var(Y_2_2);
Y_2_2 = mean(Y_2_2);

Y_2_3 = [0.07845178321871168, 0.07854704402202395, 0.07851029889815536, 0.07868503537110963, 0.07854240388831783];
var_2_3 = var(Y_2_3);
Y_2_3 = mean(Y_2_3);

Y2 = [Y_2_1, Y_2_2, Y_2_3];
err2 = [var_2_1, var_2_2, var_2_3];



figure(1);

title('Average RTT and Average Service Time over 24 hours');
hold on

%plot([1000, 1000000, 1000000000], [Y_1_1, Y_1_2, Y_1_3])
%plot([1000, 1000000, 1000000000], [Y_2_1, Y_2_2, Y_2_3])

errorbar(X,Y1,err1, '-s','MarkerSize',10,'MarkerEdgeColor','red','MarkerFaceColor','blue', 'Linewidth',2)
errorbar(X,Y2,err2, '-s','MarkerSize',10,'MarkerEdgeColor','red','MarkerFaceColor','blue', 'Linewidth',2)
%set(gca,'XScale','log');
%set(gca,'YScale','log');

grid on



xlabel('Number of Amazon Servers = 3, 16, 52');

ylabel('Mean values');

legend('Location','northeast')
legend('Average RTT','Average service time')
