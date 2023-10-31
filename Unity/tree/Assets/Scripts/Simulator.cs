using System;
using System.Collections;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.UIElements;
using UnityEngine.XR;

public class Simulator : MonoBehaviour
{
    Universe universe;
    List<Body> bodies;
    UnityEngine.Object clone;
    Body clone_body;
    CameraTrack ct;
    int time;
    OctTree root_node;
    DateTime time_start;
    DateTime time_end;
    TimeSpan total_time;
    solar_system solar = new();
    float tree_span;
    List<float> e_pots = new();
    List<float> e_kins = new();
    List<float> e_tots = new();
    List<float> x_momenta = new();
    List<float> y_momenta = new();
    List<float> z_momenta = new();
    List<float> total_momenta = new();
    bool done = true;
    float truetime;

    private void Awake()
    {
        time_start = DateTime.Now;
        bodies = new List<Body>();
        time = 0;
        universe = new Universe();
        Body copy_body = FindObjectOfType<Body>();
        ct = FindObjectOfType<CameraTrack>();
        Debug.Log("Hey");
        List<string> text = solar.Read_String("spread3.txt");
        List<string> text2 = solar.Read_String("spread5.txt");
        text.AddRange(text2);
        bodies = solar.Convert_String_To_Bodies(text, copy_body);
        for (int i = 0; i < universe.bodycount; i++)
        {
            clone = copy_body.CreateClone(copy_body);
            clone_body = clone.GetComponent<Body>();
            float min = universe.posmin;
            float max = universe.posmax;
            clone_body.ChangePosition(new Vector3(UnityEngine.Random.Range(min, max), UnityEngine.Random.Range(min, max), UnityEngine.Random.Range(min, max)));
            min = universe.velmin;
            max = universe.velmax;
            clone_body.velocity = new Vector3(UnityEngine.Random.Range(min, max), UnityEngine.Random.Range(min, max), UnityEngine.Random.Range(min, max));
            min = universe.massmin;
            max = universe.massmax;
            clone_body.ChangeMass(UnityEngine.Random.Range(min, max));
            clone_body.ChangeColor(UnityEngine.Random.Range(0, 255), UnityEngine.Random.Range(0, 255), UnityEngine.Random.Range(0, 255));
            clone_body.ChangeColor(150, 150, 150);
            clone_body.DisableLight();
            bodies.Add(clone_body);
        }
        copy_body.ChangePosition(new Vector3(Mathf.Pow(10, 30), 0f, 0f));
    }

    float FindCubeSpan()
    {
        float minX = 0f;
        float minY = 0f;
        float minZ = 0f;
        float maxX = 0f;
        float maxY = 0f;
        float maxZ = 0f;
        foreach (Body body in bodies)
        {
            if (body.position[0] > maxX) maxX = body.position[0];
            if (body.position[0] < minX) minX = body.position[0];
            if (body.position[1] > maxY) maxY = body.position[1];
            if (body.position[1] < minY) minY = body.position[1];
            if (body.position[2] > maxZ) maxZ = body.position[2];
            if (body.position[2] < minZ) minZ = body.position[2];
        }
        float dist = maxX - minX;
        if (maxY - minY > dist) dist = maxY - minY;
        if (maxZ - minZ > dist) dist = maxZ - minZ;
        return dist;
    }

    float GetKineticEnergy(Body body)
    {
        float e_kin = 0.5f * body.mass * Mathf.Pow(body.velocity.magnitude, 2);
        return e_kin;
    }

    float GetTotalKinetic()
    {
        float kinetic_energy = 0f;
        foreach (Body body in bodies) kinetic_energy += GetKineticEnergy(body);
        return kinetic_energy;
    }

    float GetPotentialEnergy(Body body)
    {
        float e_pot = 0f;
        foreach (Body b in bodies)
        {
            if (b != body)
            {
                Vector3 connector = b.position - body.position;
                float magnitude = connector.magnitude;
                e_pot -= universe.gravitational_constant * b.mass * body.mass / magnitude;  // note the minus sign
            }
        }
        return e_pot;
    }

    float GetTotalPotential()
    {
        float potential_energy = 0f;
        foreach (Body body in bodies) potential_energy += GetPotentialEnergy(body);
        return 0.5f*potential_energy;
    }

    float GetMomentum(Body body, int axis)
    {
        return body.mass * body.velocity[axis];
    }

    float GetTotalMomentum(int axis)
    {
        float momentum = 0f;
        foreach (Body body in bodies) momentum += GetMomentum(body, axis);
        return momentum;
    }

    // Update is called once per frame
    void Update()
    {
        universe.shortest_measured_distance = Mathf.Pow(10, 300);
        Debug.Log(truetime);
        Debug.Log("TIME");
        root_node = new OctTree();
        tree_span = FindCubeSpan();
        root_node.SetRoot(bodies, new Vector3(0f, 0f, 0f), tree_span+1f);
        // Debug.Log(time_end - time_start);
        // Debug.Log("^ Tree Time ^");
        foreach (Body body in bodies)
        {
            body.acceleration = body.CalculateTotalAcceleration(root_node, universe);  // could possibly be improved to just update the accel instead of always sending it back up the recursive functional loop
        }
        universe.timescale = Mathf.Pow(universe.shortest_measured_distance / universe.timescale_threshold_distance, 2);
        time += 1;
        truetime += universe.timescale * universe.timescale_factor;
        Debug.Log(universe.timescale*universe.timescale_factor);
        foreach (Body body in bodies) body.UpdateVelPos(body.acceleration, universe.timescale);  // the above idea would also let this function not take accel as an input
        if (time % 20 == 0)
        {
            float e_pot = GetTotalPotential();
            float e_kin = GetTotalKinetic();
            float e_tot = e_pot + e_kin;
            float x_mom = GetTotalMomentum(0);
            float y_mom = GetTotalMomentum(1);
            float z_mom = GetTotalMomentum(2);
            float tot_mom = x_mom + y_mom + z_mom;
            e_pots.Add(e_pot);
            e_kins.Add(e_kin);
            e_tots.Add(e_tot);
            x_momenta.Add(x_mom);
            y_momenta.Add(y_mom);
            z_momenta.Add(z_mom);
            total_momenta.Add(tot_mom);
        }
        if (truetime > 3.15576 * Mathf.Pow(10, 7) && done == false)
        {
            time_end = DateTime.Now;
            total_time = time_end - time_start;
            using (StreamWriter sw = new StreamWriter(@"F:\\Schule_Temp\\Matura\\Matura 20231015\\Nice data\\unity_tree_vs_direct\\energies_tree.txt"))
            {
                sw.WriteLine(total_time);
                sw.WriteLine("");
                foreach(float pot in e_pots) sw.WriteLine(pot);
                sw.WriteLine("");
                foreach(float kin in e_kins) sw.WriteLine(kin);
                sw.WriteLine("");
                foreach(float tot in e_tots) sw.WriteLine(tot);
                sw.WriteLine("");
                foreach(float x in x_momenta) sw.WriteLine(x);
                sw.WriteLine("");
                foreach(float y in y_momenta) sw.WriteLine(y);
                sw.WriteLine("");
                foreach(float z in z_momenta) sw.WriteLine(z);
                sw.WriteLine("");
                foreach(float tot in total_momenta) sw.WriteLine(tot);
            }
            Debug.Log("Should have written to file by now...");
            done = true;
            
        }
        // Debug.Log(time_end - time_start);
        // Debug.Log("^ Gravity Time ^");
    }   
}
