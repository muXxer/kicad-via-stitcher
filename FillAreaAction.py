#
#  FillAreaAction.py
#
#  Copyright 2017 JS Reynaud <js.reynaud@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
import pcbnew
import FillArea
import wx
import FillAreaDialog
import traceback


class FillAreaDialogEx(FillAreaDialog.FillAreaDialog):

    def onDeleteClick(self, event):
        return self.EndModal(wx.ID_DELETE)


class FillAreaAction(pcbnew.ActionPlugin):

    def defaults(self):
        self.name = "Via stitching"
        self.category = "Undefined"
        self.description = ""
        self.show_toolbar_button = False        # Optional, defaults to False
        self.icon_file_name = ""                # Optional, defaults to ""

    def Run(self):
        a = FillAreaDialogEx(None)
        a.m_SizeMM.SetValue("0.80")
        a.m_StepMM.SetValue("5.0")
        a.m_DrillMM.SetValue("0.40")
        a.m_Netname.SetValue("GND")
        a.m_ClearanceMM.SetValue("0.20")
        a.m_Debug.SetValue(False)
        a.m_Star.SetValue(True)
        modal_result = a.ShowModal()
        if modal_result == wx.ID_OK:
            try:
                fill = FillArea.FillArea()
                fill.SetStepMM(float(a.m_StepMM.GetValue()))
                fill.SetSizeMM(float(a.m_SizeMM.GetValue()))
                fill.SetDrillMM(float(a.m_DrillMM.GetValue()))
                fill.SetClearanceMM(float(a.m_ClearanceMM.GetValue()))
                fill.SetNetname(a.m_Netname.GetValue())
                fill.SetDebug(a.m_Debug.IsChecked())
                fill.SetStar(a.m_Star.IsChecked())
                fill.SetOnlyOnSelectedArea(a.m_only_selected.IsChecked())
                fill.Run()
            except Exception as exc:
                traceback.print_exc()
                wx.MessageBox(message=str(exc),
                                caption="Invalid parameter",
                                style=wx.OK | wx.ICON_ERROR)
        elif modal_result == wx.ID_DELETE:
            try:
                fill = FillArea.FillArea()
                fill.SetNetname(a.m_Netname.GetValue())
                fill.SetDebug(a.m_Debug.IsChecked())
                fill.DeleteVias()
            except Exception as exc:
                traceback.print_exc()
                wx.MessageBox(message=str(exc),
                                caption="Invalid parameter for delete",
                                style=wx.OK | wx.ICON_ERROR)
        a.Destroy()
