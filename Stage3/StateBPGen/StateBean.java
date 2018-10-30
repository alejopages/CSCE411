public class StateBean implements Comparable<StateBean>{
    private int id;
    private String name;

    public StateBean(int id, String name) {
        this.id = id;
        this.name = name;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    @Override
    public int compareTo(StateBean o) {
        return this.name.compareTo(o.getName());
    }

    @Override
    public String toString() {
        return "StateBean{" +
                "id=" + id +
                ", name='" + name + '\'' +
                '}';
    }
}
