% 定义参数
%双s型运动规律%这个运动规律还没放到路径里，代码写的还有bug
%门型轨迹，在经过直角转弯时，机器人需要先减速为0，再从0逐渐增加，机器人反复的启停则容易出现抖动现象。
clc, clear, close
q0 = 0;
q1 = 200;
vmax = 15;
amax = 10;
v0 = 0;
v1 = 0;
jmax = 10;
count = 0;

% 计算Ta、Td、Tj1、Tj2、Tv、alima、alimd等参数，他们就是时间点
if (vmax - v0) * jmax < amax^2
    if v0 > vmax
        Tj1 = 0;
        Ta = 0;
        alima = 0;
    else
        Tj1 = ((vmax - v0) / jmax)^0.5;
        Ta = 2 * Tj1;
        alima = Tj1 * jmax;
    end
else
    Tj1 = amax / jmax;
    Ta = Tj1 + (vmax - v0) / amax;
    alima = amax;
end

if (vmax - v1) * jmax < amax^2
    Tj2 = ((vmax - v1) / jmax)^0.5;
    Td = 2 * Tj2;
    alimd = Tj2 * jmax;
else
    Tj2 = amax / jmax;
    Td = Tj2 + (vmax - v1) / amax;
    alimd = amax;
end

Tv = (q1 - q0) / vmax - Ta / 2 * (1 + v0 / vmax) - Td / 2 * (1 + v1 / vmax);

% 动态调整参数，确保轨迹满足条件
if Tv <= 0
    Tv = 0;
    amax_org = amax;
    
    while Ta < 2 * Tj1 || Td < 2 * Tj2
        count = count + 1;
        amax = amax - amax_org * 0.1;
        alima = amax;
        alimd = amax;
        
        delta = (amax^4) / (jmax^2) + 2 * (v0^2 + v1^2) + amax * (4 * (q1 - q0) - 2 * amax / jmax * (v0 + v1));
        Tj1 = amax / jmax;
        Ta = (amax^2 / jmax - 2 * v0 + delta^0.5) / (2 * amax);
        Tj2 = amax / jmax;
        Td = (amax^2 / jmax - 2 * v1 + delta^0.5) / (2 * amax);
    end
end

% 计算轨迹
p = [];
vc = [];
ac = [];
jc = [];

if Tv > 0
    vlim = vmax;
    T = Tv + Ta + Td;
else
    Tv = 0;
    vlim = v0 + (Ta - Tj1) * alima;
    T = Tv + Ta + Td;
end

for t = 0:0.1:T
    if t >= 0 && t < Tj1
        % 段1：加加速度段
        q = q0 + v0 * t + jmax * t^3 / 6;
        p = [p q];
        v = v0 + jmax * t^2 / 2;
        vc = [vc v];
        a = jmax * t;
        ac = [ac a];
        jc = [jc jmax];
    elseif t >= Tj1 && t < (Ta - Tj1)
        % 段2：匀加速度段
        q = q0 + v0 * t + alima / 6 * (3 * t^2 - 3 * Tj1 * t + Tj1^2);
        p = [p q];
        v = v0 + alima * (t - Tj1 / 2);
        vc = [vc v];
        a = alima;
        ac = [ac a];
        jc = [jc 0];
    elseif t >= (Ta - Tj1) && t < Ta
        % 段3：减加速度段
        q = q0 + (vlim + v0) * Ta / 2 - vlim * (Ta - t) + jmax * (Ta - t)^3 / 6;
        p = [p q];
        v = vlim - jmax * (Ta - t)^2 / 2;
        vc = [vc v];
        a = jmax * (Ta - t);
        ac = [ac a];
        jc = [jc -jmax];
    elseif t >= Ta && t < (Ta + Tv)
        % 段4：匀速段
        q = q0 + (vlim + v0) * Ta / 2 + vlim * (t - Ta);
        p = [p q];
        v = vlim;
        vc = [vc v];
        a = 0;
        ac = [ac 0];
        jc = [jc 0];
    elseif t >= (T - Td) && t < (T - Td + Tj2)
        % 段5：加减速度段
        q = q1 - (vlim + v1) * Td / 2 + vlim * (t - T + Td) - jmax * (t - T + Td)^3 / 6;
        p = [p q];
        v = vlim - jmax * (t - T + Td)^2 / 2;
        vc = [vc v];
        a = -jmax * (t - T + Td);
        ac = [ac a];
        jc = [jc -jmax];
    elseif t >= (T - Td + Tj2) && t < (T - Tj2)
        % 段6：匀减速度段
        q = q1 - (vlim + v1) * Td / 2 + vlim * (t - T + Td) - alimd / 6 * (3 * (t - T + Td)^2 - 3 * Tj2 * (t - T + Td) + Tj2^2);
        p = [p q];
        v = vlim - alimd * (t - T + Td - Tj2 / 2);
        vc = [vc v];
        a = -alimd;
        ac = [ac a];
        jc = [jc 0];
    elseif t >= (T - Tj2) && t < T
        % 段7：减减速度段
        q = q1 - v1 * (T - t) - jmax * (T - t)^3 / 6;
        p = [p q];
        v = v1 + jmax * (T - t)^2 / 2;
        vc = [vc v];
        a = -jmax * (T - t);
        ac = [ac a];
        jc = [jc jmax];
    end
end

% 绘制位置曲线
subplot(4, 1, 1);
plot(0:0.1:T, p, 'LineWidth', 2);
xlabel('时间 (秒)');
ylabel('位置');
title('位置随时间变化');

% 绘制速度曲线
subplot(4, 1, 2);
plot(0:0.1:T, vc, 'LineWidth', 2);
xlabel('时间 (秒)');
ylabel('速度');
title('速度随时间变化');

% 绘制加速度曲线
subplot(4, 1, 3);
plot(0:0.1:T, ac, 'LineWidth', 2);
xlabel('时间 (秒)');
ylabel('加速度');
title('加速度随时间变化');
% 绘制加加速度曲线
subplot(4, 1, 4);
plot(0:0.1:T, jc, 'LineWidth', 2);
xlabel('时间 (秒)');
ylabel('加加速度');
title('加加速度随时间变化');

