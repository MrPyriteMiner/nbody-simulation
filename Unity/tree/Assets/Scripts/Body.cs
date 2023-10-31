using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public class Body : MonoBehaviour
{
    public int octant_index;
    Rigidbody rb;
    public Vector3 velocity;
    Object obj;
    Transform tf;
    Renderer ren;
    public Vector3 position;
    public Vector3 acceleration = new(0f, 0f, 0f);
    Universe uniconst = new Universe();
    public float mass;

    private void Awake()
    {
        rb = GetComponent<Rigidbody>();
        velocity = new Vector3(0f, 0f, 0f);
        obj = GetComponent<GameObject>();
        tf = GetComponent<Transform>();
        ren = GetComponent<Renderer>();
    }

    public Object CreateClone(Object obj)
    {
        Object clone = Instantiate(obj);
        return clone;
    }

    public void ChangePosition(Vector3 pos)
    {
        position = pos;
        rb = GetComponent<Rigidbody>();
        rb.MovePosition(position / uniconst.length_scalar);
    }

    public void ChangeVelocity(Vector3 vel)
    {
        velocity = vel;
    }

    public void ChangeMass(float mass_new)
    {
        mass = mass_new;
        rb.mass = mass;
        double radius = Mathf.Pow(mass, 1f / 12f) / uniconst.length_scalar * 100000000 + 0.3;
        tf.localScale = new Vector3((float)radius, (float)radius, (float)radius);
    }
    public void ChangeColor(int r, int g, int b)
    {
        Color color = new Color(r / 255f, g / 255f, b / 255f, 1f);
        ren.material.color = color;
        ren.material.SetColor("_EmissionColor", color);
    }
    public void DisableLight()
    {
        ren.material.SetColor("_EmissionColor", Color.black);
    }

    public void SetOctant(int oct_index)
    {
        octant_index = oct_index;
    }

    /// <summary>
    /// use leapfrog integration for a tiny improvement in accuracy
    /// </summary>
    /// <param name="acceleration"></param>
    /// <param name="timestep"></param>
    public void UpdateVelPos(Vector3 acceleration, float timestep)
    {
        velocity += acceleration * timestep * uniconst.timescale_factor;
        position += velocity * timestep * uniconst.timescale_factor;
        rb.MovePosition(position / uniconst.length_scalar);
    }

    /// <summary>
    /// calculates the acceleration of the body; G is the gravitational constant
    /// </summary>
    /// <param name="bodies"></param>
    /// <param name="G"></param>
    /// <returns></returns>
    public Vector3 CalculateTotalAcceleration(OctTree node, Universe uni)
    {
        Vector3 acceleration_sum = new(0f, 0f, 0f);
        if (node.terminal is true)
        {
            if (node.bodies.Count == 0) return new Vector3(0f, 0f, 0f);
            if (node.bodies[0] == this) return new Vector3(0f, 0f, 0f);
            return CalculateAcceleration(node, uni);
        }
        float magnitude = (node.center_of_mass - position).magnitude;
        if (magnitude / node.sidelength < uni.estimation_threshold)
        {
            foreach (OctTree child in node.children)
            {
                acceleration_sum += CalculateTotalAcceleration(child, uni);
            }
            return acceleration_sum;
        }
        return CalculateAcceleration(node, uni);
    }

    public Vector3 CalculateAcceleration(OctTree n, Universe uni)
    {
        Vector3 connector = n.center_of_mass - position;
        float distance = connector.magnitude;
        if (uni.shortest_measured_distance > distance) uni.shortest_measured_distance = distance;
        return n.total_mass * uni.gravitational_constant * connector / (distance * distance * distance);
    }
}
