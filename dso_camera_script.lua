function Camera_LockClick(sender)
   local adresses = getAddressList()
   local camera = adresses[0]
   local smoke = adresses[1]
   if sender.Checked then
      camera.Active = true
      smoke.Active = true
   else
      camera.Active = false
      smoke.Active = false
   end
 end
 
 function Camera_CameraSetClick(sender)
   local camera = getAddressList()[0]
   local value = tonumber(Camera.CameraValue.Text)
   if camera.Active then
      camera.Active = false
      camera.Value = value
      camera.Active = true
   else
      camera.Value = value
   end
 end
 
 function Camera_SmokeSetClick(sender)
   local smoke = getAddressList()[1]
   local value = tonumber(Camera.SmokeValue.Text)
   if smoke.Active then
      smoke.Active = false
      smoke.Value = value
      smoke.Active = true
   else
      smoke.Value = value
   end
 end
 
 function Camera_FogDisableClick(sender)
    if Camera.FogDisable.Checked then
       getAddressList()[2].Value = -1500
       getAddressList()[3].Active = true
       getAddressList()[3].Value = -1500
       getAddressList()[2].Active = true
 
    else
       getAddressList()[2].Active = false
       getAddressList()[3].Active = false
 
    end
 end
 
 function GetTheProcessList()
    local TempTable = {}
    local SL=createStringlist()
    local indx = 0
    getProcesslist(SL)
    for i=0,strings_getCount(SL)-1 do
      local entry = strings_getString(SL,i)
      local processname = entry:sub(10,255)
      local PID = tonumber('0x'..entry:sub(1,8))
      if processname == "dro_client64.exe" then
         TempTable[indx] = {PID, processname}
         indx = indx + 1
         end
      end
   return TempTable
 end
 
 function Camera_ScannowClick(sender)
    local id = getOpenedProcessID()
    local list = Camera.CEListBox1
    Camera.Execute.Enabled = true
    items = listbox_getItems(list)
    strings_clear(items)
    Camera.Height = 330
    local TempTable = GetTheProcessList()
    local index = 0
    for y in pairs (TempTable) do
       index = index+1
    end
    for i=0, index-1 do
        local text = TempTable[i][1].." - "..TempTable[i][2]
        strings_add(items, text)
        if id == TempTable[i][1] then
           Camera.CEListBox1.ItemIndex = i
        end
    end
 
    showMessage("Processes found: "..index)
 end
 
 function Camera_ExecuteClick(sender)
    --Camera.Lock.Checked = true
    local id = getOpenedProcessID()
    local TempTable = GetTheProcessList()
    local index = 0
    for y in pairs (TempTable) do
       index = index+1
    end
    for i=0, index-1 do
        openProcess(TempTable[i][1])
        Camera_SmokeSetClick(sender)
        Camera_CameraSetClick(sender)
        if Camera.FogDisable.Checked then
           getAddressList()[2].Value = -150
           getAddressList()[2].Active = true
        else
           getAddressList()[2].Active = false
        end
    end
    openProcess(id)
 end
 
 function Camera_CEListBox1DblClick(sender)
    local sel = Camera.CEListBox1.ItemIndex
    if sel ~= nil and sel ~= -1 then
       local TempTable = GetTheProcessList()
       openProcess(TempTable[sel][1])
       local text = TempTable[sel][1].." - "..TempTable[sel][2]
       showMessage("Process   "..text.."   opened")
       local camera = getAddressList()[0]
       local smoke = getAddressList()[1]
       local fog = getAddressList()[2]
       Camera.CameraValue.Text = 34
       Camera.SmokeValue.Text = 0
       Camera.FogValue = -150
       camera.Active = false
       smoke.Active = false
       fog.Active = false
       Camera.Lock.Checked = false
       Camera.FogDisable.Checked = false
    end
 end
 
 function Camera_FogSetClick(sender)
    local fog = getAddressList()[2]
    local value = tonumber(Camera.FogValue.Text)
    if fog.Active then
      fog.Active = false
      fog.Value = value
      fog.Active = true
    else
      fog.Value = value
    end
 end
 
 
 function checkKeys()
    key_1()
    key_2()
 end
 
 function key_1()
    local id = getOpenedProcessID()
    local curr = getForegroundProcess()
    if curr ~= id then
       openProcess(curr)
    end
    getAddressList()[0].Value = tonumber(Camera.CameraValue.Text)
    getAddressList()[0].Active = true
    if getAddressList()[1].Active then
       Camera.Lock.Checked = true
    end
    if curr ~= id then
       openProcess(id)
    end
 end
 
 function key_2()
    local id = getOpenedProcessID()
    local curr = getForegroundProcess()
    if curr ~= id then
       openProcess(curr)
    end
    getAddressList()[1].Value = tonumber(Camera.SmokeValue.Text)
    getAddressList()[1].Active = true
    if getAddressList()[0].Active then
       Camera.Lock.Checked = true
    end
    if curr ~= id then
       openProcess(id)
    end
 end
 
 function key_3()
    local id = getOpenedProcessID()
    local curr = getForegroundProcess()
    if curr ~= id then
       openProcess(curr)
    end
    Camera.FogDisable.Checked = true
    Camera_FogDisableClick(nil)
    if curr ~= id then
       Camera.FogDisable.Checked = false
       openProcess(id)
    end
 end
 
 
 RequiredCEVersion=7,3
 if (getCEVersion==nil) or (getCEVersion()<RequiredCEVersion) then
   messageDialog('Please install Cheat Engine '..RequiredCEVersion, mtError, mbOK)
   closeCE()
 end
 
 getAutoAttachList().add("dro_client64.exe")
 gPlaySoundOnAction=false
 Camera.fixDPI()
 Camera.show()
 Camera.Heiht = 140
 
 createHotkey(key_1, {VK_CONTROL, VK_1})
 createHotkey(key_2, {VK_CONTROL, VK_2})
 createHotkey(key_3, {VK_CONTROL, VK_3})
 
 function AboutClick()
   showMessage(gAboutText)
 end
 gAboutText=[[This trainer was made by Cheat Engine
 www.cheatengine.org]]
 
 function CloseClick()
   --called by the close button onClick event, and when closing the form
   closeCE()
   return caFree --onClick doesn't care, but onClose would like a result
 end
 
 --TRAINERGENERATORSTOP--
 
 function Camera_FormResize(sender)
     if Camera.Execute.Enabled == false then
        if Camera.Height > 140 then
           Camera.Height = 140
        end
     else
         if Camera.Height > 290 then
           Camera.Height = 290
        end
     end
     if Camera.Width > 225 then
        Camera.Width = 225
     end
 end
 