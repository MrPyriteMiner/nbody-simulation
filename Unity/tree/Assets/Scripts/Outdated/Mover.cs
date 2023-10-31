using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public class Mover : MonoBehaviour
{
    Rigidbody rb;
    Vector3 velocity;
    int time;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    private void Awake()
    {
        rb = GetComponent<Rigidbody>();
        velocity = new Vector3(1f, 1f, 1f);
        time = 0;
    }

    // Update is called once per frame
    void Update()
    {
        rb.MovePosition(new Vector3((float)Math.Sin(time/30), (float)Math.Cos(time/30), 0));
        time++;
    }
}
