using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Sets a bunch of universal constants
/// </summary>
public class Universe
{
    public float gravitational_constant = 6.6743f * Mathf.Pow(10, -11);
    public int bodycount = 0;
    public float posmin = -2f * Mathf.Pow(10, 11);
    public float posmax = 2f * Mathf.Pow(10, 11);
    public float velmin = -0.01f * Mathf.Pow(10, 4);
    public float velmax = 0.01f * Mathf.Pow(10, 4);
    public float massmin = 0.1f * Mathf.Pow(10, 24);
    public float massmax = 1f * Mathf.Pow(10, 26);
    public float timescale = 1f;
    public float timescale_threshold_distance = Mathf.Pow(10, 3);
    public float timescale_factor = Mathf.Pow(2, -32);
    public float length_scalar = 10000000000f;
    public float estimation_threshold = 4;
    public float shortest_measured_distance = Mathf.Pow(10, 300);
}
