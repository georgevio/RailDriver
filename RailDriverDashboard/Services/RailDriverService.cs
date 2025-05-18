using System;
using System.Runtime.InteropServices;

namespace RailDriverDashboard.Services
{
    public class RailDriverService
    {
        private const string RailDriverDllPath = @"C:\Program Files (x86)\Steam\steamapps\common\RailWorks\plugins\RailDriver64.dll";

        [DllImport(RailDriverDllPath)]
        private static extern IntPtr GetControllerList(); 

        [DllImport(RailDriverDllPath)]
        private static extern float GetControllerValue(string controllerName); 

        [DllImport(RailDriverDllPath)]
        private static extern float GetCurrentControllerValue(); 

        [DllImport(RailDriverDllPath, CharSet = CharSet.Ansi)]
        private static extern IntPtr GetLocoName(); 

        [DllImport(RailDriverDllPath)]
        private static extern int GetNextRailDriverId(); 

        [DllImport(RailDriverDllPath)]
        private static extern int GetRailDriverConnected();

        [DllImport(RailDriverDllPath)]
        private static extern int GetRailDriverGetId(); 

        [DllImport(RailDriverDllPath)]
        private static extern int GetRailDriverGetType(); 

        [DllImport(RailDriverDllPath)]
        private static extern float GetRailDriverValue(); 

        [DllImport(RailDriverDllPath)]
        private static extern float GetRailSimCombinedThrottleBrake(); 

        [DllImport(RailDriverDllPath)]
        private static extern int GetRailSimConnected();

        [DllImport(RailDriverDllPath)]
        private static extern int GetRailSimLocoChanged(); 

        [DllImport(RailDriverDllPath)]
        private static extern float GetRailSimValue(); 

        [DllImport(RailDriverDllPath)]
        private static extern int IsLocoSet(); 

        [DllImport(RailDriverDllPath)]
        private static extern void SetRailDriverConnected(int value);

        [DllImport(RailDriverDllPath, EntryPoint = "SetLocoName", CharSet = CharSet.Ansi)]
        private static extern void SetLocoName(string locoName);

        public string[] inGetControllerList()
        {
            IntPtr controllerListPtr = GetControllerList();
            string controllerList = Marshal.PtrToStringAnsi(controllerListPtr);
            return controllerList?.Split(new[] { "::" }, StringSplitOptions.RemoveEmptyEntries) ?? Array.Empty<string>();
        }

        public float inGetControllerValue(string controllerName)
        {
            // Ensure controllerName is trimmed and formatted correctly
            controllerName = controllerName.Trim(); // Removes any unwanted spaces
            Console.WriteLine($"Fetching value for controller: '{controllerName}'");

            return GetControllerValue(controllerName);
        }

        public float inGetCurrentControllerValue()
        {
            return GetCurrentControllerValue();
        }

        public string inGetLocoName()
        {
            IntPtr locoNamePtr = GetLocoName();
            return Marshal.PtrToStringAnsi(locoNamePtr) ?? string.Empty;
        }

        public int inGetNextRailDriverId()
        {
            return GetNextRailDriverId();
        }

        public int inGetRailDriverConnected()
        {
            return GetRailDriverConnected();
        }

        public int inGetRailDriverGetId()
        {
            return GetRailDriverGetId();
        }

        public int inGetRailDriverGetType()
        {
            return GetRailDriverGetType();
        }

        public float inGetRailDriverValue()
        {
            return GetRailDriverValue();
        }

        public float inGetRailSimCombinedThrottleBrake()
        {
            return GetRailSimCombinedThrottleBrake();
        }

        public int inGetRailSimConnected()
        {
            return GetRailSimConnected();
        }

        public int inGetRailSimLocoChanged()
        {
            return GetRailSimLocoChanged();
        }

        public float inGetRailSimValue()
        {
            return GetRailSimValue();
        }

        public int inIsLocoSet()
        {
            return IsLocoSet();
        }

        public void inSetRailDriverConnected(int value)
        {
            SetRailDriverConnected(value);
        }

        public void inSetLocoName(string locoName)
        {
            SetLocoName(locoName);
        }
    }
}