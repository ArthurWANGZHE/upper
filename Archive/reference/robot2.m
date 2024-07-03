clear; clc;

x=zeros(68*68*68,1);
y=zeros(68*68*68,1);
z=zeros(68*68*68,1);
cosb=0;
cosc=0;
cosd=0;
m=1;
z1 = 0;
y1 = 0;
x1 = 0;
for i=1:2:300
    for j=1:2:300
        for k=1:2:300
            [cosb,cosc,cosd]=Delta_Inversesolution2(k,j,i);
            [x1,y1,z1]=Delta_Inversesolution(k,j,i);
            if(abs(cosb)<0.34&&abs(cosc)<0.34&&abs(cosd)<0.34&&z1>-430)
                m = m+1;
                [x(m),y(m),z(m)]= Delta_Inversesolution(k,j,i);
            end
        end
    end
end
v = [x,y,z];
shp = alphaShape(v);
plot(shp);
axis square;
%%plot3(x, y, z, 'b.'); % 使用蓝色点表示茄子的位置
%%hold on; % 保持图形，以便绘制下一个茄子的位置
%%xlabel('x'); % x轴标签
%%ylabel('y'); % y轴标签
%%zlabel('z'); % z轴标签
%%grid on; % 显示网格
%%axis square; % 设置坐标轴比例为等比例