using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class OctTree
{
    OctTree parent;
    public List<Body> bodies;
    public OctTree[] children;
    public Vector3 center_of_mass;
    public float total_mass;
    public float sidelength;
    Vector3 position;
    public bool terminal;

    private void Awake()
    {
        center_of_mass = new Vector3(0f, 0f, 0f);
        total_mass = 0f;
    }

    public void SetLineage(OctTree parent_node, List<Body> local_bodies, Vector3 oct_position)
    {
        parent = parent_node;
        bodies = local_bodies;
        position = oct_position;
        sidelength = parent_node.sidelength / 2;
        terminal = true;
        SetCenterOfMass();
        if (bodies.Count > 1) Expand();
    }

    public void SetRoot(List<Body> all_bodies, Vector3 root_position, float default_sidelength)
    {
        bodies = all_bodies;
        position = root_position;
        ScaleSize(default_sidelength);
        terminal = true;
        SetCenterOfMass();
        if (bodies.Count > 1) Expand();
    }

    public void SetCenterOfMass()
    {
        foreach (Body body in bodies)
        {
            center_of_mass += body.position*body.mass;
            total_mass += body.mass;
        }
        center_of_mass /= total_mass;
    }

    public void Expand()
    {
        terminal = false;
        children = new OctTree[8];
        List<List<Body>> partition_list = PartitionBodies();
        for (int i = 0; i < 8; i++)
        {
            float quarter_sidelength = sidelength / 4;
            Vector3 new_position = position - new Vector3(quarter_sidelength, quarter_sidelength, quarter_sidelength);
            if (i % 2 >= 1) new_position += new Vector3(quarter_sidelength * 2, 0, 0);
            if (i % 4 >= 2) new_position += new Vector3(0, quarter_sidelength * 2, 0);
            if (i % 8 >= 4) new_position += new Vector3(0, 0, quarter_sidelength * 2);
            children[i] = new OctTree();
            children[i].SetLineage(this, partition_list[i], new_position);
        }

    }

    public List<List<Body>> PartitionBodies()
    {
        List<List<Body>> partitioned_list = new();
        for (int i = 0; i < 8; i++) partitioned_list.Add(new List<Body>());
        for (int i = 0; i < bodies.Count; i++)
        {
            int index = 0;
            Body body = bodies[i];
            if (body.position[0] >= position[0]) index += 1;
            if (body.position[1] >= position[1]) index += 2;
            if (body.position[2] >= position[2]) index += 4;
            partitioned_list[index].Add(body);
        }
        return partitioned_list;
    }

    public void ScaleSize(float default_sidelength)
    {
        sidelength = default_sidelength;
        foreach (Body body in bodies)
        {
            while (body.position[0]>sidelength || body.position[1]>sidelength || body.position[2]>sidelength)
            {
                sidelength *= 2;
            }
        }
    }
}
