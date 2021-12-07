clear; close all; clc;

%Takes existing pics of Duke and converts them into m x n matrices, finds
%their average and reshapes it into a vector, x.
%
%Only run this create or reset 'Sum', 'x', and/or 'count'

dukeDir = '../data/duke';
m = 168;
n = 192;

dukePics = dir(fullfile(dukeDir,'*.jpg'));
Sum = zeros(n,m);
for k = 1:length(dukePics)
    duke = dukePics(k).name;
    dukeParks = fullfile(dukeDir, duke); %dukeParks is full name of duke
    A = imresize(double(rgb2gray(imread(dukeParks))), [n,m]);
    %pcolor(flipud(A)), shading interp, colormap(gray)
    Sum = Sum + A;
end
Avg = Sum / length(dukePics);
count = length(dukePics);
pcolor(flipud(Avg)), shading interp, colormap(gray)
x = reshape(Avg,n*m,1);
save('dukeAvg.mat', 'Sum','x', 'count')

