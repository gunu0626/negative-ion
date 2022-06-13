clear

currentfolder = pwd;
targetfolder = uigetdir();
cd(targetfolder);

subdirNum = str2double(questdlg('In which order ldf files are listed?','Numbers of sub directory', '0','1','2','2'));

listCounter = 0;

if subdirNum == 0
    filelisting = dir('*.ldf');
    
    allSubdirs = dir('*');
    dirFlags = [allSubdirs.isdir];
    subfolders = allSubdirs(dirFlags);
    
    
    for j=1:length(filelisting)
        rawdata = fileread(filelisting(j).name);
        posNe       = [strfind(rawdata,'<Ne>')+4,strfind(rawdata,'</Ne>')-1];
        poskTe      = [strfind(rawdata,'<kTe>')+5,strfind(rawdata,'</kTe>')-1];
        poseedf_Ne  = [strfind(rawdata,'<eedf_Ne>')+9,strfind(rawdata,'</eedf_Ne>')-1];
        poseedf_kTe = [strfind(rawdata,'<eedf_kTe>')+10,strfind(rawdata,'</eedf_kTe>')-1];
        posVf       = [strfind(rawdata,'<Vf>')+4,strfind(rawdata,'</Vf>')-1];
        posVp       = [strfind(rawdata,'<Vp>')+4,strfind(rawdata,'</Vp>')-1];
        
        pos = [posVp, posVf, posNe, poskTe, poseedf_Ne, poseedf_kTe];
        
        for k=1:length(pos)/2
            for l=1:pos(2*k)-pos(2*k-1)+1
                var(l) = rawdata(pos(2*k-1)+l-1); %#ok<SAGROW>
            end
            varOut(k) = str2double(var); %#ok<SAGROW>
            clear var
        end
        
        clear rawX
        clear X
        clear tempX
        posX = [strfind(rawdata,'<vec label="energy">;')+21,strfind(rawdata,'</eedf_data>')-16];
        for k=1:posX(2)-posX(1)
            rawX(k) = rawdata(posX(1)+k-1); %#ok<SAGROW>
        end
        posXseg = strfind(rawX,';');
        k = 0;
        l = 1;
        while l<length(posXseg)+1
            k = k+1;
            if k == posXseg(l)
                X(l) = str2double(tempX); %#ok<SAGROW>
                l = l+1;
                clear tempX
            else
                tempX(k) = rawX(k); %#ok<SAGROW>
            end
        end
        
        clear rawY
        posY = [strfind(rawdata,'<vec label="EEDF">;')+19,strfind(rawdata,'<vec label="EEDF_error">')-20];
        for k=1:posY(2)-posY(1)
            rawY(k) = rawdata(posY(1)+k-1); %#ok<SAGROW>
        end
        posYseg = strfind(rawY,';');
        k = 0;
        l = 1;
        while l<length(posYseg)+1
            k = k+1;
            if k == posYseg(l)
                Y(l) = str2double(tempY); %#ok<SAGROW>
                l = l+1;
                clear tempY
            else
                tempY(k) = rawY(k); %#ok<SAGROW>
            end
        end
        
        dataOutput(j+listCounter) = struct('ExperimentSet',filelisting(j).name, ...
            'Vp', varOut(1),'Vf', varOut(2),'Ne', varOut(3),'kTe', varOut(4),'Ne_eedf', varOut(5),'kTe_eedf', varOut(6)...
            ,'eepf_X', X,'eepf_Y', Y); %#ok<SAGROW>
        
        fieldname = strrep(strrep(strrep(strrep(['eepf_',filelisting(j).name], ' ', '_'),'-','m'),'.ldf',''),'.','_');
        
        for k=1:length(X)
            eepfOutput(k).energy = X(k); %#ok<SAGROW>
        end
        for k=1:length(Y)
            eepfOutput(k).(fieldname) = Y(k);
        end
        
    end
        listCounter = listCounter+j;
        
elseif subdirNum == 1
    allSubdirs = dir('*');
    dirFlags = [allSubdirs.isdir];
    subfolders = allSubdirs(dirFlags);
    
    for i=3:length(subfolders)
        cd([subfolders(i).folder,'\',subfolders(i).name]);
        filelisting = dir('*.ldf');
        
        for j=1:length(filelisting)
            rawdata = fileread(filelisting(j).name);
            posNe       = [strfind(rawdata,'<Ne>')+4,strfind(rawdata,'</Ne>')-1];
            poskTe      = [strfind(rawdata,'<kTe>')+5,strfind(rawdata,'</kTe>')-1];
            poseedf_Ne  = [strfind(rawdata,'<eedf_Ne>')+9,strfind(rawdata,'</eedf_Ne>')-1];
            poseedf_kTe = [strfind(rawdata,'<eedf_kTe>')+10,strfind(rawdata,'</eedf_kTe>')-1];
            posVf       = [strfind(rawdata,'<Vf>')+4,strfind(rawdata,'</Vf>')-1];
            posVp       = [strfind(rawdata,'<Vp>')+4,strfind(rawdata,'</Vp>')-1];
            
            pos = [posVp, posVf, posNe, poskTe, poseedf_Ne, poseedf_kTe];
            
            for k=1:length(pos)/2
                for l=1:pos(2*k)-pos(2*k-1)+1
                    var(l) = rawdata(pos(2*k-1)+l-1); %#ok<SAGROW>
                end
                varOut(k) = str2double(var); %#ok<SAGROW>
                clear var
            end
            
            clear rawX
            clear X
            clear tempX
            posX = [strfind(rawdata,'<vec label="energy">;')+21,strfind(rawdata,'</eedf_data>')-16];
            for k=1:posX(2)-posX(1)
                rawX(k) = rawdata(posX(1)+k-1); %#ok<SAGROW>
            end
            posXseg = strfind(rawX,';');
            k = 0;
            l = 1;
            while l<length(posXseg)+1
                k = k+1;
                if k == posXseg(l)
                    X(l) = str2double(tempX); %#ok<SAGROW>
                    l = l+1;
                    clear tempX
                else
                    tempX(k) = rawX(k); %#ok<SAGROW>
                end
            end
            
            clear rawY
            posY = [strfind(rawdata,'<vec label="EEDF">;')+19,strfind(rawdata,'<vec label="EEDF_error">')-20];
            for k=1:posY(2)-posY(1)
                rawY(k) = rawdata(posY(1)+k-1); %#ok<SAGROW>
            end
            posYseg = strfind(rawY,';');
            k = 0;
            l = 1;
            while l<length(posYseg)+1
                k = k+1;
                if k == posYseg(l)
                    Y(l) = str2double(tempY); %#ok<SAGROW>
                    l = l+1;
                    clear tempY
                else
                    tempY(k) = rawY(k); %#ok<SAGROW>
                end
            end
            
            dataOutput(j+listCounter) = struct('ExperimentGroup',subfolders(i).name,'ExperimentSet',filelisting(j).name, ...
                'Vp', varOut(1),'Vf', varOut(2),'Ne', varOut(3),'kTe', varOut(4),'Ne_eedf', varOut(5),'kTe_eedf', varOut(6)...
                ,'eepf_X', X,'eepf_Y', Y); %#ok<SAGROW>
            
            fieldname = strrep(strrep(strrep(strrep(['eepf_',subfolders(i).name,' ',filelisting(j).name], ' ', '_'),'-','m'),'.ldf',''),'.','_');
            
            for k=1:length(X)
                eepfOutput(k).energy = X(k); %#ok<SAGROW>
            end
            for k=1:length(Y)
                eepfOutput(k).(fieldname) = Y(k);
            end
            
        end
        listCounter = listCounter+j;
    end
    
else
    
    secondallSubdirs = dir('*');
    dirFlags = [secondallSubdirs.isdir];
    secondsubfolders = secondallSubdirs(dirFlags);
    
    for m=3:length(secondsubfolders)
        cd([secondsubfolders(m).folder,'\',secondsubfolders(m).name]);
        
        allSubdirs = dir('*');
        dirFlags = [allSubdirs.isdir];
        subfolders = allSubdirs(dirFlags);
        
        for i=3:length(subfolders)
            cd([subfolders(i).folder,'\',subfolders(i).name]);
            filelisting = dir('*.ldf');
            
            for j=1:length(filelisting)
                rawdata = fileread(filelisting(j).name);
                posNe       = [strfind(rawdata,'<Ne>')+4,strfind(rawdata,'</Ne>')-1];
                poskTe      = [strfind(rawdata,'<kTe>')+5,strfind(rawdata,'</kTe>')-1];
                poseedf_Ne  = [strfind(rawdata,'<eedf_Ne>')+9,strfind(rawdata,'</eedf_Ne>')-1];
                poseedf_kTe = [strfind(rawdata,'<eedf_kTe>')+10,strfind(rawdata,'</eedf_kTe>')-1];
                posVf       = [strfind(rawdata,'<Vf>')+4,strfind(rawdata,'</Vf>')-1];
                posVp       = [strfind(rawdata,'<Vp>')+4,strfind(rawdata,'</Vp>')-1];
                
                pos = [posVp, posVf, posNe, poskTe, poseedf_Ne, poseedf_kTe];
                
                for k=1:length(pos)/2
                    for l=1:pos(2*k)-pos(2*k-1)+1
                        var(l) = rawdata(pos(2*k-1)+l-1); %#ok<SAGROW>
                    end
                    varOut(k) = str2double(var); %#ok<SAGROW>
                    clear var
                end
                
                clear rawX
                clear X
                clear tempX
                posX = [strfind(rawdata,'<vec label="energy">;')+21,strfind(rawdata,'</eedf_data>')-16];
                for k=1:posX(2)-posX(1)
                    rawX(k) = rawdata(posX(1)+k-1); %#ok<SAGROW>
                end
                posXseg = strfind(rawX,';');
                k = 0;
                l = 1;
                while l<length(posXseg)+1
                    k = k+1;
                    if k == posXseg(l)
                        X(l) = str2double(tempX); %#ok<SAGROW>
                        l = l+1;
                        clear tempX
                    else
                        tempX(k) = rawX(k); %#ok<SAGROW>
                    end
                end
                
                clear rawY
                posY = [strfind(rawdata,'<vec label="EEDF">;')+19,strfind(rawdata,'<vec label="EEDF_error">')-20];
                for k=1:posY(2)-posY(1)
                    rawY(k) = rawdata(posY(1)+k-1); %#ok<SAGROW>
                end
                posYseg = strfind(rawY,';');
                k = 0;
                l = 1;
                while l<length(posYseg)+1
                    k = k+1;
                    if k == posYseg(l)
                        Y(l) = str2double(tempY); %#ok<SAGROW>
                        l = l+1;
                        clear tempY
                    else                    tempY(k) = rawY(k); %#ok<SAGROW>
                        
                    end
                end
                
                dataOutput(j+listCounter) = struct('ExperimentGroupA',secondsubfolders(m).name,'ExperimentGroupB',subfolders(i).name,'ExperimentSet',filelisting(j).name, ...
                    'Vp', varOut(1),'Vf', varOut(2),'Ne', varOut(3),'kTe', varOut(4),'Ne_eedf', varOut(5),'kTe_eedf', varOut(6)...
                    ,'eepf_X', X,'eepf_Y', Y); %#ok<SAGROW>
                
                fieldname = strrep(strrep(strrep(strrep(['eepf_',secondsubfolders(m).name,' ',subfolders(i).name,' ',filelisting(j).name], ' ', '_'),'-','m'),'.ldf',''),'.','_');
                
                for k=1:length(X)
                    eepfOutput(k).energy = X(k); %#ok<SAGROW>
                end
                for k=1:length(Y)
                    eepfOutput(k).(fieldname) = Y(k);
                end
            end
            listCounter = listCounter+j;
        end        
    end
end

cd(currentfolder);

writetable(struct2table(rmfield(dataOutput,{'eepf_X','eepf_Y'})),'DataOutput.xlsx','Sheet',1)
writetable(struct2table(eepfOutput),'DataOutput.xlsx','Sheet',2)
    