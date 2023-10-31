using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;
using System.IO;
using static System.Console;
using UnityEngine.UIElements;
using System.Linq;

public class solar_system
{
    public List<string> Read_String(string filename)
    {
        string path = "F:\\Schule_Temp\\Matura\\Momentum Test\\" + filename;
        Debug.Log(path);
        string[] bodies_text = File.ReadAllLines(@path);
        Debug.Log(bodies_text);
        List<string> bodies = new();
        foreach (string txt in bodies_text) 
        {
            bodies.Add(txt);
        }
        return bodies;
    }

    public List<Body> Convert_String_To_Bodies(List<string> bodies, Body body)
    {
        List<Body> final_bodies = new();
        for (int i = 0; i < bodies.Count; i++)
        {
            string str = bodies[i];
            string[] split = str.Split(' ');
            Object clone = body.CreateClone(body);
            Body clone_body = clone.GetComponent<Body>();
            clone_body.ChangePosition(new Vector3(float.Parse(split[1]), float.Parse(split[2]), float.Parse(split[3])));
            clone_body.ChangeVelocity(new Vector3(float.Parse(split[4]), float.Parse(split[5]), float.Parse(split[6])));
            clone_body.ChangeMass(float.Parse(split[7]));
            clone_body.ChangeColor(int.Parse(split[8]), int.Parse(split[9]), int.Parse(split[10]));
            if (split[0] != "Sun:") clone_body.DisableLight();
            final_bodies.Add(clone_body);
        }
        return final_bodies;
    }
}