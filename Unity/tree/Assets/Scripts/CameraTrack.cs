using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraTrack : MonoBehaviour
{
    Transform tf;

    private void Awake()
    {
        tf = GetComponent<Transform>();
    }

    public void UpdateCamera(Vector3 cameraPosition)
    {
        tf.position = cameraPosition;
    }
}
